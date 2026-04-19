---
title: Lulc Backend
emoji: 🔥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# LULC Recognition Backend

FastAPI backend for the Deep Learning Land Use & Land Cover Recognition System.

## Setup

### 1. Install Dependencies

Using uv (recommended):
```bash
cd backend
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 2. Add Model Files

Place your trained model files in the `models/` directory:

```bash
# Create models directory if it doesn't exist
mkdir -p models

# Copy your trained models here:
# - models/eurosat.pth
# - models/mrlnset.pth
# - models/patternnet.pth
```

The models should be saved as PyTorch state_dict files:
```python
torch.save(model.module.state_dict(), 'models/eurosat.pth')
```

### 3. Run the Server

```bash
uv run app.py
```

The server will start on `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST `/predict`
Predict LULC class for an image.

**Parameters:**
- `file` (multipart): Image file (JPEG or PNG)
- `model_type` (string): Model to use (`eurosat`, `mlrsnet`, `patternnet`)

**Response:**
```json
{
  "predicted_class": "Permanent Crop",
  "class_index": 6,
  "confidence": 0.95,
  "inference_time_ms": 25.5,
  "model_type": "eurosat",
  "image_info": {
    "format": "JPEG"
  },
  "explain_maps": {
    "Saliency": "data:image/jpeg;base64,...",
    "GradCAM": "data:image/jpeg;base64,...",
    "GradCAM++": "data:image/jpeg;base64,...",
    "LIME": "data:image/jpeg;base64,..."
  }
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "device": "cpu",
  "models_available": ["mlrsnet", "patternnet", "eurosat"]
}
```

### GET `/info`
Get system information.

**Response:**
```json
{
  "system": "Deep Learning LULC Recognition",
  "version": "1.0.0",
  "models": ["eurosat", "mlrsnet", "patternnet"],
  "architecture": "Explainable CNN",
  "parameters_approx": 400000,
  "flops_approx": 106000000,
  "device": "cpu"
}
```

## Using Your Trained Models

The backend expects state_dict files saved from PyTorch models:

1. Place your model files in the `models/` directory with these exact names:
   - `eurosat.pth` (EuroSAT Fold 4)
   - `mrlnset.pth` (MLRSNet Fold 3)
   - `patternnet.pth` (PatternNet Fold 3)

2. Models should be saved as state_dict:
   ```python
   torch.save(model.module.state_dict(), 'models/eurosat.pth')
   ```

3. Ensure your model has the correct output classes:
   - EuroSAT: 10 classes
   - MLRSNet: 25 classes
   - PatternNet: 59 classes

4. Restart the server for changes to take effect

## Architecture

- **Preprocessor**: Smart remote sensing preprocessing pipeline
  - Dynamic Resize: EuroSAT images only resized to 64x64 if they exceed that size.
  - Standard Resize: 224x224 for other models.
  - Convert to tensor
  - Normalize with ImageNet statistics
- **Explainers**: Integrated Saliency, GradCAM, GradCAM++, and LIME for model transparency.
- **Error Handling**: Validation for image formats, file sizes, and device compatibility


## Performance Notes

- Inference time is measured in milliseconds
- First inference may be slower (model loading)
- Subsequent inferences are cached and faster
- GPU support available (automatically detected)
