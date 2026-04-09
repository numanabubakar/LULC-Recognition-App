# LULC Recognition Dashboard - Setup Guide

Complete setup instructions for the Deep Learning Land Use & Land Cover (LULC) Recognition System with FastAPI backend and Next.js frontend.

## Project Structure

```
project/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main FastAPI application
│   ├── model_loader.py     # Modular model loading system
│   ├── preprocessing.py    # Image preprocessing pipeline
│   ├── class_mappings.py   # Dataset class definitions
│   ├── pyproject.toml      # Python dependencies
│   └── models/             # Directory for .pth model files
├── app/                    # Next.js frontend
│   ├── page.tsx            # Main dashboard page
│   ├── layout.tsx          # Root layout
│   └── globals.css         # Theme and styling
├── components/             # React components
│   ├── DatasetSelector.tsx # Dataset selection sidebar
│   ├── ImageUploadZone.tsx # Drag-and-drop image uploader
│   ├── NeuralNetworkLoader.tsx # Loading animation
│   ├── PredictionResults.tsx   # Results display
│   └── TechnicalSpecs.tsx  # Technical specifications footer
└── package.json            # Node dependencies
```

## Backend Setup (FastAPI + PyTorch)

### Prerequisites
- Python 3.9 or higher
- pip or uv (recommended)

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies using uv (recommended):**
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Add trained models:**
   
   Place your trained PyTorch state_dict models in the `models/` directory:
   ```bash
   mkdir -p models
   # Copy your models:
   # - models/eurosat.pth (EuroSAT Fold 4)
   # - models/mrlnset.pth (MLRSNet Fold 3)
   # - models/patternnet.pth (PatternNet Fold 3)
   ```

4. **Start the FastAPI server:**
   ```bash
   uv run app.py
   ```
   
   The server will start on `http://localhost:8000`
   
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Frontend Setup (Next.js)

### Prerequisites
- Node.js 18+ or 20+
- pnpm (or npm/yarn)

### Installation

1. **Install frontend dependencies:**
   ```bash
   pnpm install
   ```

2. **Run development server:**
   ```bash
   pnpm dev
   ```
   
   The app will be available at `http://localhost:3000`

3. **Update API endpoint (if needed):**
   
   In `app/page.tsx`, update the fetch URL if your backend is running on a different port:
   
   ```typescript
   const response = await fetch('http://localhost:8000/predict', {
   ```

## Running the Complete System

### Development Mode (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
uv run app.py
```

**Terminal 2 - Frontend:**
```bash
pnpm dev
```

Then open your browser to `http://localhost:3000`

### Production Deployment

#### Backend (FastAPI)
```bash
cd backend
uv run uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend (Next.js)
```bash
pnpm build
pnpm start
```

## Using Your Own Models

To replace the mock models with your trained PyTorch models:

1. **Ensure your models have the correct architecture:**
   ```python
   class MyModel(nn.Module):
       def __init__(self, num_classes):
           super().__init__()
           # Your architecture here
       
       def forward(self, x):
           # Returns logits
           return logits
   ```

2. **Save model state dict:**
   ```python
   torch.save(model.state_dict(), 'models/eurosat_fold4.pth')
   ```

3. **Required number of classes:**
   - EuroSAT: 10 classes
   - MLRSNet: 25 classes
   - PatternNet: 59 classes

4. **Update preprocessing if needed:**
   
   In `backend/preprocessing.py`, modify the normalization if your model uses different ImageNet stats or custom preprocessing.

## API Endpoints

### POST `/predict`
Predict LULC class for an image.

**Request:**
```
multipart/form-data
- file: (Binary image file)
- model_type: "eurosat" | "mlrsnet" | "patternnet"
```

**Response:**
```json
{
  "predicted_class": "Permanent Crop",
  "class_index": 6,
  "confidence": 0.95,
  "inference_time_ms": 25.5,
  "model_type": "eurosat",
  "image_info": {
    "width": 512,
    "height": 512,
    "format": "JPEG"
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
  "models_available": ["eurosat", "mlrsnet", "patternnet"]
}
```

### GET `/info`
Get system information and specs.

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

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
- The backend already has CORS enabled for all origins
- Check that both frontend and backend are running
- Verify the backend URL in `app/page.tsx` matches your server

### Connection Refused
If you get "Connection refused" errors:
- Make sure the FastAPI backend is running on port 8000
- Check firewall settings
- Try accessing http://localhost:8000/health directly

### Model Loading Issues
If models fail to load:
- Verify model files exist in `backend/models/`
- Check that model state dicts match the architecture
- Ensure correct number of output classes for each model

### GPU Support
- Models will automatically use GPU if available
- Check the `/health` endpoint to see current device ("cuda" or "cpu")
- To force CPU: Set `CUDA_VISIBLE_DEVICES=""` before running backend

## Performance Notes

- **First inference:** ~100-500ms (includes model loading)
- **Subsequent inferences:** ~25-50ms (cached model)
- **Preprocessing:** ~5-10ms
- **Image sizes:** Accepts up to 10MB files
- **Resolution:** Automatically resizes to 224×224

## Development Tips

### Adding New Datasets
1. Add class mappings in `backend/class_mappings.py`
2. Add model config in `backend/model_loader.py`
3. Update frontend dataset options in `components/DatasetSelector.tsx`

### Customizing Theme
- Edit color variables in `app/globals.css`
- All colors use CSS variables (--primary, --accent, etc.)
- Dark mode is enabled by default

### Monitoring
- Check backend logs for inference details
- Use `/health` endpoint to monitor system status
- Monitor frontend Network tab in browser DevTools for API calls

## License & Attribution

This is a Final Year Project implementation of LULC recognition using benchmark datasets:
- EuroSAT
- MLRSNet
- PatternNet

## Support

For issues or questions, refer to:
- Backend documentation: `backend/README.md`
- Component source files for implementation details
- FastAPI docs: http://localhost:8000/docs
