# Model Integration Guide

This guide explains how to integrate your trained PyTorch models with the LULC Recognition system.

## Model Requirements

Your models should be saved as PyTorch state_dict files (not full models or TorchScript):

```python
# How your models were saved:
torch.save(model.module.state_dict(), 'models/eurosat.pth')
torch.save(model.module.state_dict(), 'models/mrlnset.pth')
torch.save(model.module.state_dict(), 'models/patternnet.pth')
```

## File Locations

Place your model files in the `backend/models/` directory:

```
backend/
├── models/
│   ├── eurosat.pth      # EuroSAT Fold 4 state_dict
│   ├── mrlnset.pth      # MLRSNet Fold 3 state_dict
│   └── patternnet.pth   # PatternNet Fold 3 state_dict
├── app.py
├── model_loader.py
└── ...
```

## Expected Output Classes

Ensure your models have the correct number of output classes:

- **EuroSAT**: 10 classes
  - Annual Crop, Forest, Herbaceous Vegetation, Highway, Industrial, Pasture, Permanent Crop, Residential, River, Sea Lake

- **MLRSNet**: 25 classes
  - Airplane, Airport, Bare Land, Baseball Diamond, Basketball Court, Beach, Bridge, Buildings, Chaparral, Church, Clouds, Commercial Area, Dense Residential, Desert, Farmland, Forest, Golf Course, Ground Track Field, Harbor, Intersection, Island, Lake, Meadow, Medium Residential, Mobile Home Park

- **PatternNet**: 59 classes
  - (Various patterns including Airplane, Airfield, Airport, etc.)

## Current Model Loader Implementation

The `model_loader.py` file loads your state_dict files:

```python
# Current implementation in model_loader.py
state_dict = torch.load(model_path, map_location=self.device)
```

This loads the state_dict directly. The models are expected to be:
1. Saved as `state_dict()` (not full model)
2. Compatible with the inference pipeline
3. Tested on 224×224 RGB images with ImageNet normalization

## Important Notes

1. **State Dict Only**: The system expects state_dict files only, not full PyTorch models or TorchScript modules.

2. **Device Mapping**: Models are automatically loaded to CPU or GPU based on availability:
   ```python
   state_dict = torch.load(model_path, map_location=self.device)
   ```

3. **Inference Speed**: The preprocessing pipeline (resize to 224×224 + ImageNet normalization) should take ~5-10ms, with model inference taking 15-50ms depending on model complexity.

4. **Error Handling**: If a model file is missing, the backend will raise a clear error:
   ```
   FileNotFoundError: Model file not found: backend/models/eurosat.pth
   ```

## Testing Your Models

To verify your models work correctly:

1. Start the backend:
   ```bash
   cd backend
   uv run app.py
   ```

2. Test with the demo client:
   ```bash
   cd backend
   python demo_client.py
   ```

3. Or use curl:
   ```bash
   curl -X POST "http://localhost:8000/predict" \
     -F "file=@test_image.jpg" \
     -F "model_type=eurosat"
   ```

## Troubleshooting

### Model file not found
- Check the model filename matches exactly (case-sensitive):
  - `eurosat.pth`
  - `mrlnset.pth`
  - `patternnet.pth`

### Model loading fails
- Verify the file is a valid PyTorch state_dict
- Check the file is not corrupted: `torch.load(path)` should work in Python

### Incorrect predictions
- Verify preprocessing matches your training:
  - Resize to 224×224
  - ImageNet normalization: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
- Check class order matches your training

### Out of memory errors
- Models are loaded once and cached
- For large models, consider model quantization or pruning
- GPU memory can be freed by restarting the backend

## Advanced: Modifying Model Architecture

If you need to change the model architecture in the backend:

1. Edit `backend/model_loader.py`:
   ```python
   # Define your architecture
   class YourModel(nn.Module):
       def __init__(self, num_classes):
           super().__init__()
           # your layers here
       
       def forward(self, x):
           return x
   
   # In load_model():
   model = YourModel(num_classes=num_classes)
   model.load_state_dict(state_dict)
   ```

2. Update class counts in `backend/class_mappings.py` if needed

3. Restart the backend

## Production Deployment

When deploying to production:

1. Ensure model files are included in Docker build (docker-compose.yml includes volume mount)
2. Models should be downloaded/copied before starting the container
3. Consider model caching strategies for scale
4. Monitor inference latency and adjust timeouts as needed

For detailed deployment information, see `DEPLOYMENT.md`.
