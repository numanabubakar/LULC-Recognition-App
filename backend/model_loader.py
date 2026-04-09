"""Modular model loader for LULC recognition system."""

import torch
import torch.nn as nn
from pathlib import Path
from class_mappings import get_num_classes
from models_arch import AMFRNet


class ModelLoader:
    """Loads and manages PyTorch models for different datasets."""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def load_model(self, model_type: str) -> nn.Module:
        """
        Load a model state_dict for the specified dataset.
        
        Args:
            model_type: One of "eurosat", "mlrsnet", or "patternnet"
            
        Returns:
            PyTorch model on appropriate device
        """
        model_map = {
            "eurosat": "eurosat.pth",
            "mlrsnet": "mlrsnet.pth",
            "patternnet": "patternnet.pth",
        }
        
        if model_type not in model_map:
            raise ValueError(f"Unknown model type: {model_type}")
        
        filename = model_map[model_type]
        model_path = self.models_dir / filename
        
        # Check if model file exists
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {model_path}. "
                f"Please ensure the model file is at: backend/models/{filename}"
            )
        
        # Load checkpoint object from disk
        print(f"[model_loader] loading checkpoint: {model_path}")
        loaded_obj = torch.load(model_path, map_location=self.device)

        # Case 1: full nn.Module was saved (recommended)
        if isinstance(loaded_obj, nn.Module):
            model = loaded_obj

        # Case 2: plain state_dict was saved (expected in this project)
        elif isinstance(loaded_obj, dict) and all(
            isinstance(v, torch.Tensor) for v in loaded_obj.values()
        ):
            # Prefer checkpoint classifier size if available; fallback to mapping.
            fc_bias = loaded_obj.get("fc.bias")
            if isinstance(fc_bias, torch.Tensor) and fc_bias.ndim == 1:
                num_classes = int(fc_bias.shape[0])
            else:
                num_classes = get_num_classes(model_type)
            model = AMFRNet(num_classes=num_classes)
            missing_keys, unexpected_keys = model.load_state_dict(loaded_obj, strict=True)
            if missing_keys or unexpected_keys:
                raise RuntimeError(
                    f"Checkpoint key mismatch for '{model_type}'. "
                    f"Missing keys: {missing_keys}; Unexpected keys: {unexpected_keys}"
                )
            print(
                f"[model_loader] state_dict loaded for '{model_type}' "
                f"with num_classes={num_classes}"
            )

        # Case 3: Any other unexpected object type
        else:
            raise RuntimeError(
                f"Unsupported model object type loaded from {model_path}: "
                f"{type(loaded_obj)}. Expected nn.Module or state_dict."
            )
        
        # Move model to device if it's a nn.Module
        if isinstance(model, nn.Module):
            model = model.to(self.device)
            model.eval()
            print(
                f"[model_loader] model ready: {model.__class__.__name__} "
                f"on {self.device}"
            )
        
        return model
    
    def get_device(self) -> torch.device:
        """Get the device where models are running."""
        return self.device


# Global model loader instance
_model_loader = None

def get_model_loader(models_dir: str = "models") -> ModelLoader:
    """Get or create the global model loader instance."""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader(models_dir=models_dir)
    return _model_loader
