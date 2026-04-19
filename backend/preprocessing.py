"""Image preprocessing pipeline for remote sensing images."""

import torch
from torchvision import transforms
from PIL import Image
from io import BytesIO
from typing import Tuple


class LULCPreprocessor:
    """Preprocessing pipeline for LULC remote sensing images."""
    
    def __init__(self, image_size: int = 224):
        """
        Initialize preprocessor with standard ImageNet normalization.
        
        Args:
            image_size: Target size for resizing (default 224x224)
        """
        self.image_size = image_size
        self.default_transforms = transforms.Compose([
            transforms.Resize((image_size, image_size), interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],  # ImageNet normalization
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Keep for backwards compatibility if needed
        self.transforms = self.default_transforms
        
    def get_transforms(self, model_type: str, image_width: int, image_height: int):
        """Get the appropriate transforms based on model type and image size."""
        if model_type == "eurosat":
            if image_width > 64 or image_height > 64:
                return transforms.Compose([
                    transforms.Resize((64, 64), interpolation=transforms.InterpolationMode.BILINEAR),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
            else:
                return transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
        return self.default_transforms
    
    def preprocess(self, image_bytes: bytes, model_type: str = None) -> torch.Tensor:
        """
        Preprocess image from bytes to normalized tensor.
        
        Args:
            image_bytes: Image file as bytes
            model_type: The model type to use for preprocessing logic
            
        Returns:
            Normalized image tensor of shape (1, 3, H, W)
        """
        # Load image from bytes
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        # Apply transforms
        transform = self.get_transforms(model_type, image.width, image.height)
        image_tensor = transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def get_image_info(self, image_bytes: bytes) -> dict:
        """Get basic info about the image."""
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format or "UNKNOWN",
        }


# Global preprocessor instance
_preprocessor = None

def get_preprocessor(image_size: int = 224) -> LULCPreprocessor:
    """Get or create the global preprocessor instance."""
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = LULCPreprocessor(image_size=image_size)
    return _preprocessor
