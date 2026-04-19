# LULC Recognition Dashboard

A professional, research-oriented Deep Learning dashboard for Land Use & Land Cover (LULC) classification using benchmark datasets. Built with Next.js frontend and FastAPI backend, featuring three state-of-the-art datasets: EuroSAT, MLRSNet, and PatternNet.

## 🎯 Features

### Frontend (Next.js + React)
- **Scientific Laboratory Aesthetic**: Slate-950 dark theme with indigo accents
- **Dataset Selection**: Sidebar navigator for three benchmark datasets
- **Drag-and-Drop Upload**: Intuitive image upload with instant preview
- **Neural Network Animation**: Sophisticated loading state simulating pixel processing
- **Real-time Results Display**:
  - Predicted class label with index
  - Radial and linear confidence gauges
  - Performance metrics (inference time, parameters)
  - Technical specifications (FLOPs, architecture type)
- **Responsive Design**: Works seamlessly on desktop and mobile

### Backend (FastAPI + PyTorch)
- **Explainability Suite**: Built-in support for GradCAM, GradCAM++, Saliency maps, and LIME explanations
- **Smart Preprocessing**: Conditional resizing logic (EuroSAT images only resized if > 64x64)
- **CORS Enabled**: Ready for production deployment with secure origins
- **Production Ready**: Supports actual trained PyTorch state_dict models

## 🚀 Quick Start

### Prerequisites
- **Backend**: Python 3.9+
- **Frontend**: Node.js 18+ or 20+
- **Package Managers**: uv (Python), pnpm (Node)

### 1. Start Backend

```bash
cd backend
uv sync
# Place your trained models in backend/models/ directory:
# - eurosat.pth
# - mrlnset.pth
# - patternnet.pth
uv run app.py
```

Backend runs on: `http://localhost:8000`

### 2. Start Frontend

```bash
pnpm install
pnpm dev
```

Frontend runs on: `http://localhost:3000`

### 3. Use the Dashboard

1. Open http://localhost:3000 in your browser
2. Select a benchmark dataset (EuroSAT, MLRSNet, or PatternNet)
3. Upload a satellite/aerial image (JPEG or PNG)
4. Click "Run Inference" to get predictions
5. View detailed results with confidence scores

## 📦 Project Structure

```
.
├── app/
│   ├── page.tsx              # Main dashboard
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Theme & styles
├── components/
│   ├── DatasetSelector.tsx   # Dataset picker
│   ├── ImageUploadZone.tsx   # Upload zone
│   ├── NeuralNetworkLoader.tsx # Loading animation
│   ├── PredictionResults.tsx  # Results display
│   └── TechnicalSpecs.tsx    # Tech specs footer
├── backend/
│   ├── app.py                # FastAPI server
│   ├── model_loader.py       # Model management
│   ├── preprocessing.py      # Image pipeline
│   ├── class_mappings.py     # Class definitions
│   └── models/               # PyTorch state_dict files
├── SETUP.md                  # Detailed setup guide
└── README.md                 # This file
```

## 📊 Supported Datasets

### EuroSAT (Fold 4)
- **Classes**: 10 (Annual Crop, Forest, Urban, etc.)
- **Description**: European satellite imagery classification
- **Image Size**: Typically 64×64, resized to 224×224

### MLRSNet (Fold 3)
- **Classes**: 25 (multi-class remote sensing)
- **Description**: Multi-spectral remote sensing benchmark
- **Applications**: Land cover mapping, environmental monitoring

### PatternNet (Fold 3)
- **Classes**: 59 (high-resolution benchmark)
- **Description**: High-resolution aerial imagery
- **Applications**: Detailed land use classification

## 🔧 Technical Specifications

| Metric | Value |
|--------|-------|
| **Architecture** | Explainable CNN |
| **Parameters** | ~400K |
| **FLOPs** | ~106M |
| **Input Size** | 224×224 |
| **Inference Time** | ~25ms |
| **Normalization** | ImageNet (μ=[0.485, 0.456, 0.406], σ=[0.229, 0.224, 0.225]) |
| **Device** | CPU/GPU (auto-detected) |

## 🔌 API Endpoints

### POST `/predict`
Predict LULC class for an image.

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@image.jpg" \
  -F "model_type=eurosat"
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
Health check.

### GET `/info`
System information and specifications.

## 🧠 Using Your Own Models

Replace mock models with your trained PyTorch models:

1. **Prepare your model:**
   ```python
   model = YourModel(num_classes=10)
   torch.save(model.state_dict(), 'backend/models/eurosat_fold4.pth')
   ```

2. **Required output classes:**
   - EuroSAT: 10
   - MLRSNet: 25
   - PatternNet: 59

3. **Adjust preprocessing (if needed):**
   - Edit `backend/preprocessing.py`
   - Update normalization statistics

## 🎨 Theme Customization

Edit color variables in `app/globals.css`:

```css
--primary: #6366f1        /* Indigo */
--accent: #818cf8         /* Light Indigo */
--background: #0f172a     /* Slate-950 */
--foreground: #f1f5f9     /* Slate-100 */
```

## 📱 Responsive Design

- **Mobile**: Single column layout, optimized touch
- **Tablet**: 2-3 column grid
- **Desktop**: Full 4-column layout with sidebar

## 🚢 Production Deployment

### Backend
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
pnpm build
pnpm start
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Backend has CORS enabled; check frontend API URL |
| Connection refused | Ensure backend runs on port 8000 |
| Model not found | Run `uv run create_mock_models.py` in backend |
| GPU not detected | Set `CUDA_VISIBLE_DEVICES=""` to force CPU |

## 📚 Documentation

- **Backend Details**: See `backend/README.md`
- **Setup Instructions**: See `SETUP.md`
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 🏗️ Architecture Overview

```
┌─────────────────────────┐
│   Next.js Frontend      │
│  (React Components)     │
│  • Dataset Selector     │
│  • Image Upload         │
│  • Results Display      │
└──────────────┬──────────┘
               │ HTTP/REST
               │
┌──────────────▼──────────┐
│   FastAPI Backend       │
│  (Python/PyTorch)       │
│  • Model Loader         │
│  • Preprocessing        │
│  • Inference Engine     │
└─────────────────────────┘
               │
               │ Model Loading
               │
        ┌──────▼──────┐
        │ PyTorch     │
        │ Models      │
        │ (.pth)      │
        └─────────────┘
```

## 📋 Requirements

### Backend
```
fastapi==0.104.1
uvicorn==0.24.0
torch==2.1.1
torchvision==0.16.1
pillow==10.1.0
python-multipart==0.0.6
pydantic==2.5.0
```

### Frontend
```
next@^15.0.0
react@^19.0.0
tailwindcss@^4.0.0
lucide-react@^latest
```

## 🎓 Academic Context

This is a Final Year Project implementation demonstrating:
- Deep learning for remote sensing
- Real-time inference systems
- Production-ready ML deployment
- Modern full-stack development
- Professional UI/UX for scientific applications

## 📄 License

Academic project for educational and research purposes.

## ✉️ Contact & Support

For questions or issues, refer to:
- Backend documentation: `backend/README.md`
- Setup guide: `SETUP.md`
- Component documentation in source files

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready
