"""Model architectures used for checkpoint loading in inference."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBNReLU(nn.Module):
    def __init__(self, in_c, out_c, k, s=1, p=0, groups=1, dilation=1):
        super().__init__()
        self.conv = nn.Conv2d(
            in_c,
            out_c,
            k,
            stride=s,
            padding=p,
            groups=groups,
            bias=False,
            dilation=dilation,
        )
        self.bn = nn.BatchNorm2d(out_c)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class SEBlock(nn.Module):
    def __init__(self, channels, reduction=16):
        super().__init__()
        hidden = max(channels // reduction, 4)
        self.fc1 = nn.Linear(channels, hidden)
        self.fc2 = nn.Linear(hidden, channels)

    def forward(self, x):
        b, c, _, _ = x.size()
        y = x.mean(dim=(2, 3))
        y = F.relu(self.fc1(y), inplace=True)
        y = torch.sigmoid(self.fc2(y))
        y = y.view(b, c, 1, 1)
        return x * y


class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super().__init__()
        padding = (kernel_size - 1) // 2
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        y = torch.cat([avg_out, max_out], dim=1)
        y = torch.sigmoid(self.conv(y))
        return x * y


class CrossScaleCorrelation(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv = nn.Conv2d(channels * 2, channels, kernel_size=1, bias=True)

    def forward(self, x):
        _, _, h, w = x.size()
        small = F.avg_pool2d(x, kernel_size=2, stride=2)
        small_up = F.interpolate(small, size=(h, w), mode="bilinear", align_corners=False)
        y = torch.cat([x, small_up], dim=1)
        y = torch.sigmoid(self.conv(y))
        return x * y


class HierarchicalSESpatialBlock(nn.Module):
    def __init__(self, channels, se_reduction=16):
        super().__init__()
        self.se = SEBlock(channels, reduction=se_reduction)
        self.spatial = SpatialAttention(kernel_size=7)
        self.crossscale = CrossScaleCorrelation(channels)

    def forward(self, x):
        y = self.se(x)
        y = self.spatial(y)
        y = self.crossscale(y)
        return y


class AsymResidualDenseBlock(nn.Module):
    def __init__(self, in_c, out_c, growth=32, layers=3):
        super().__init__()
        self.dense_layers = nn.ModuleList()
        c = in_c
        for _ in range(layers):
            self.dense_layers.append(
                nn.Sequential(
                    nn.Conv2d(c, growth, (1, 3), padding=(0, 1), bias=False),
                    nn.BatchNorm2d(growth),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(growth, growth, (3, 1), padding=(1, 0), bias=False),
                    nn.BatchNorm2d(growth),
                    nn.ReLU(inplace=True),
                )
            )
            c += growth

        self.proj = nn.Conv2d(c, out_c, kernel_size=1, bias=False)
        self.bn = nn.BatchNorm2d(out_c)
        self.res = nn.Conv2d(in_c, out_c, kernel_size=1, bias=False) if in_c != out_c else None

    def forward(self, x):
        feats = [x]
        for layer in self.dense_layers:
            feats.append(layer(torch.cat(feats, dim=1)))
        out = self.proj(torch.cat(feats, dim=1))
        out = self.bn(out)
        res = self.res(x) if self.res is not None else x
        return F.relu(out + res, inplace=True)


class DynamicPathSelection(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.gate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_c, 16),
            nn.ReLU(inplace=True),
            nn.Linear(16, 2),
        )
        self.path1 = AsymResidualDenseBlock(in_c, out_c)
        self.path2 = nn.Sequential(
            ConvBNReLU(in_c, out_c, k=3, s=1, p=2, dilation=2),
            SEBlock(out_c),
        )

    def forward(self, x):
        b = x.size(0)
        w_logits = self.gate(x)
        w = F.softmax(w_logits, dim=1)
        w1 = w[:, 0].view(b, 1, 1, 1)
        w2 = w[:, 1].view(b, 1, 1, 1)
        f1 = self.path1(x)
        f2 = self.path2(x)
        return w1 * f1 + w2 * f2


class AMFRNet(nn.Module):
    def __init__(self, num_classes: int):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(3, 64, 7, 2, 3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2, 1),
        )
        self.block1 = AsymResidualDenseBlock(64, 64)
        self.hse1 = HierarchicalSESpatialBlock(64)
        self.paths = DynamicPathSelection(64, 128)
        self.hse2 = HierarchicalSESpatialBlock(128)
        self.block3 = AsymResidualDenseBlock(128, 256)
        self.fc = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.stem(x)
        x = self.block1(x)
        x = self.hse1(x)
        x = self.paths(x)
        x = self.hse2(x)
        x = self.block3(x)
        x = F.adaptive_avg_pool2d(x, (1, 1))
        x = x.view(x.size(0), -1)
        return self.fc(x)
