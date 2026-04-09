# LULC Recognition Dashboard - Architecture Documentation

Comprehensive technical architecture of the Deep Learning Land Use & Land Cover Recognition System.

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    User Browser (Client)                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Next.js React Application (Frontend)            │  │
│  │                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │  DataSet     │  │  Image       │  │  Results     │   │  │
│  │  │  Selector    │  │  Upload      │  │  Display     │   │  │
│  │  │  (Sidebar)   │  │  (DnD)       │  │  (Card)      │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │  Neural Net  │  │  Performance │  │  Technical   │   │  │
│  │  │  Loader      │  │  Metrics     │  │  Specs       │   │  │
│  │  │  (Animation) │  │  (Gauges)    │  │  (Footer)    │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │                                                            │  │
│  │  Theme: Slate-950 Dark + Indigo Accents                  │  │
│  │  Framework: Next.js 15 + React 19                        │  │
│  │  Styling: Tailwind CSS 4 + Custom CSS                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                        HTTP POST /predict
                     (multipart form-data)
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│              FastAPI Backend Server (Python)                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         FastAPI Application (app.py)                   │   │
│  │                                                        │   │
│  │  Routes:                                              │   │
│  │  • POST /predict - Main inference endpoint           │   │
│  │  • GET /health - Server health check                 │   │
│  │  • GET /info - System information                    │   │
│  │                                                        │   │
│  │  Middleware:                                          │   │
│  │  • CORS - Enable cross-origin requests               │   │
│  │  • Error handlers - Validate & handle errors         │   │
│  └────────────────────────────────────────────────────────┘   │
│                     │                │                          │
│         ┌───────────▼──────┐   ┌─────▼──────────────┐          │
│         │  Model Loader    │   │  Image             │          │
│         │  (model_loader   │   │  Preprocessing     │          │
│         │  .py)            │   │  (preprocessing    │          │
│         │                  │   │  .py)              │          │
│         │ • Caches models  │   │ • Resize to 224×224
│         │ • Load on demand │   │ • Normalize (ImageNet)
│         │ • GPU support    │   │ • Convert to tensor
│         └────────┬─────────┘   └─────┬──────────────┘
│                  │                   │
│                  └───────┬───────────┘
│                          │
│                          ▼
│         ┌─────────────────────────────────┐
│         │   PyTorch Inference Engine      │
│         │                                 │
│         │ • Forward pass through CNN      │
│         │ • Softmax for probabilities     │
│         │ • Performance tracking          │
│         │ • Device management (CPU/GPU)   │
│         └────────────┬────────────────────┘
│                      │
│                      ▼
│         ┌─────────────────────────────────┐
│         │   PyTorch Model Layer           │
│         │                                 │
│         │ model.eval() mode               │
│         │ no_grad() context               │
│         │ Device: cuda/cpu                │
│         └────────────┬────────────────────┘
│                      │
└──────────────────────┼─────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────┐
    │     Model Files Storage               │
    ├──────────────────────────────────────┤
    │  models/                             │
    │  ├── eurosat_fold4.pth               │
    │  ├── mlrsnet_fold3.pth               │
    │  └── patternnet_fold3.pth            │
    │                                      │
    │  Each .pth contains:                 │
    │  • Model state dictionary            │
    │  • Weights and biases                │
    │  • Architecture parameters           │
    └──────────────────────────────────────┘
```

## Frontend Component Hierarchy

```
App (page.tsx)
├── Header
│   ├── Logo + Title
│   └── Description
│
├── Main Grid (2 columns: sidebar + content)
│   │
│   ├── Sidebar
│   │   └── DatasetSelector
│   │       ├── EuroSAT (10 classes)
│   │       ├── MLRSNet (25 classes)
│   │       └── PatternNet (59 classes)
│   │
│   └── Content Area
│       ├── Upload Section
│       │   └── ImageUploadZone
│       │       ├── Drag-and-drop area
│       │       ├── File input
│       │       └── Image preview
│       │
│       ├── Action Button
│       │   └── "Run Inference" button
│       │
│       ├── Loading State
│       │   └── NeuralNetworkLoader
│       │       ├── Animated network
│       │       ├── Orbiting nodes
│       │       └── Pulse animation
│       │
│       ├── Results Section (conditional)
│       │   └── PredictionResults
│       │       ├── Predicted Class Card
│       │       │   ├── Class label
│       │       │   ├── Class index
│       │       │   └── Check icon
│       │       │
│       │       ├── Confidence Gauge
│       │       │   ├── Percentage display
│       │       │   ├── Radial progress
│       │       │   └── Linear progress bar
│       │       │
│       │       └── Performance Metrics
│       │           ├── Inference time
│       │           ├── Model type
│       │           ├── Image size
│       │           └── Image format
│       │
│       ├── Clear Button (conditional)
│       │   └── "Upload Another Image"
│       │
│       └── Technical Specs
│           └── TechnicalSpecs
│               ├── Architecture: Explainable CNN
│               ├── Parameters: ~400K
│               ├── FLOPs: ~106M
│               ├── Input size: 224×224
│               └── Normalization: ImageNet
│
└── Footer
    └── Version info
```

## Backend Component Architecture

### app.py - Main Application
```python
FastAPI()
├── Middleware
│   └── CORSMiddleware
│
├── Routes
│   ├── POST /predict
│   │   ├── Validate image
│   │   ├── Preprocess image
│   │   ├── Load model
│   │   ├── Run inference
│   │   └── Format response
│   │
│   ├── GET /health
│   │   └── Return server status
│   │
│   └── GET /info
│       └── Return system specs
│
└── Error Handlers
    ├── HTTPException handlers
    ├── Validation errors
    └── Inference errors
```

### model_loader.py - Model Management
```python
ModelLoader (Singleton Pattern)
├── __init__()
│   ├── Set device (cuda/cpu)
│   ├── Load model cache
│   └── Create models dir
│
├── load_model(model_type)
│   ├── Check cache
│   ├── Load state dict
│   ├── Move to device
│   └── Set eval mode
│
├── SUPPORTED_MODELS
│   ├── eurosat -> 10 classes
│   ├── mlrsnet -> 25 classes
│   └── patternnet -> 59 classes
│
└── get_device()
    └── Return cuda/cpu device
```

### preprocessing.py - Image Pipeline
```python
LULCPreprocessor
├── __init__(image_size=224)
│   └── Setup transform pipeline
│
├── preprocess(image_bytes)
│   ├── Load image from bytes
│   ├── Resize to 224×224
│   ├── Convert to tensor
│   ├── Normalize (ImageNet)
│   └── Add batch dimension
│
├── get_image_info(image_bytes)
│   └── Return {width, height, format}
│
└── Transform Pipeline
    ├── Resize (bilinear interpolation)
    ├── ToTensor (convert to [0,1])
    └── Normalize (μ, σ)
```

### class_mappings.py - Class Definitions
```python
Class Mappings
├── EUROSAT_CLASSES (10 classes)
│   ├── 0: Annual Crop
│   ├── 1: Forest
│   ├── ...
│   └── 9: Sea Lake
│
├── MLRSNET_CLASSES (25 classes)
│   ├── 0: Airplane
│   ├── 1: Bare soil
│   ├── ...
│   └── 24: Tennis court
│
├── PATTERNNET_CLASSES (59 classes)
│   ├── 0: Airplane
│   ├── 1: Baseball diamond
│   ├── ...
│   └── 58: Winding road
│
└── Helper functions
    ├── get_class_label(model_type, index)
    └── get_num_classes(model_type)
```

## Data Flow Diagram

### Prediction Flow
```
User uploads image
        │
        ▼
Browser sends FormData
├── file: Image (binary)
└── model_type: "eurosat" | "mlrsnet" | "patternnet"
        │
        ▼ (HTTP POST /predict)
FastAPI receives request
        │
        ▼ (app.py)
Validate image format
        │
        ├─ Not JPEG/PNG? → Return 400 error
        │
        ▼
Validate file size
        │
        ├─ > 10MB? → Return 413 error
        │
        ▼
Validate model_type
        │
        ├─ Invalid? → Return 400 error
        │
        ▼ (model_loader.py)
Load model (or use cached)
├─ Check if already loaded
├─ If not: Load state dict from .pth
├─ Move to device (cuda/cpu)
└─ Set to eval mode
        │
        ▼ (preprocessing.py)
Preprocess image
├─ Load image from bytes
├─ Convert to RGB
├─ Resize to 224×224
├─ Convert to tensor
├─ Normalize (ImageNet stats)
└─ Add batch dimension [1, 3, 224, 224]
        │
        ▼ (PyTorch)
Forward pass
├─ Input tensor → Model
├─ Conv + ReLU + MaxPool layers
├─ Flatten and fully connected
└─ Output logits [1, num_classes]
        │
        ▼
Softmax to probabilities
├─ Sum to 1.0
└─ Get confidence scores
        │
        ▼
Extract prediction
├─ Max probability
├─ Class index
├─ Confidence value
└─ Inference time (ms)
        │
        ▼ (class_mappings.py)
Get class label
├─ Look up in class dictionary
└─ Return human-readable name
        │
        ▼ (app.py)
Format response
{
  "predicted_class": "Permanent Crop",
  "class_index": 6,
  "confidence": 0.95,
  "inference_time_ms": 25.5,
  "model_type": "eurosat",
  "image_info": {...}
}
        │
        ▼ (HTTP 200)
Send to browser
        │
        ▼ (React)
Update state
├─ setResult(prediction)
├─ setIsLoading(false)
└─ setError(null)
        │
        ▼
Render PredictionResults
├─ Display class label
├─ Show confidence gauge
├─ Display performance metrics
└─ Update technical specs
```

## Performance Characteristics

### Latency Breakdown
```
Total: ~25-50ms (typical)

Preprocessing:    5-10ms  (image resize + normalization)
Model Loading:    0ms     (cached after first load)
Forward Pass:     10-20ms (depends on device)
Post-processing:  1-2ms   (softmax, argmax)
Network:          5-10ms  (HTTP roundtrip)
```

### Memory Usage
```
Model Memory:     ~20MB per model
Image Buffer:     ~10MB (max file size)
Runtime State:    ~100MB (batch + caches)
Device:           Fits in CPU/GPU RAM
```

### Throughput
```
Sequential:       ~20-40 images/second (CPU)
Sequential:       ~50-100 images/second (GPU)
Batch (if added): ~100-200 images/second (GPU)
```

## Technology Stack

### Frontend
```
Framework:        Next.js 15
UI Library:       React 19
Styling:          Tailwind CSS 4
Icons:            Lucide React
Images:           Next.js Image component
State:            React Hooks
HTTP Client:      fetch API
```

### Backend
```
Framework:        FastAPI 0.104
Server:           Uvicorn
ML Framework:     PyTorch 2.1
Image Proc:       Pillow 10
Validation:       Pydantic 2
```

### Deployment
```
Frontend:         Vercel / Node.js
Backend:          Docker / Cloud VM / AWS
Database:         None (stateless)
Cache:            In-memory (Python)
```

## Security Considerations

### Input Validation
- File type validation (JPEG/PNG only)
- File size limits (10MB max)
- Image dimension checks
- Model type validation

### CORS
- Configured for all origins (consider limiting in production)
- Allows credentials if needed
- Standard HTTP methods

### Error Handling
- No sensitive info in error messages
- Proper HTTP status codes
- Client-side validation
- Try-catch blocks

## Scalability Improvements

### Horizontal Scaling
1. **Load Balancer**: Distribute requests across servers
2. **Stateless Design**: Each request is independent
3. **Model Caching**: Replicate model cache across instances

### Vertical Scaling
1. **GPU Support**: Automatic detection and usage
2. **Batch Processing**: Process multiple images
3. **Model Optimization**: Use quantization/pruning

### Caching Strategy
1. **Model Cache**: Cache-per-instance (already implemented)
2. **Result Cache**: Could cache common predictions
3. **CDN**: Frontend assets via CDN

## Future Enhancements

1. **Batch Predictions**: Accept multiple images at once
2. **Model Ensembling**: Combine predictions from multiple models
3. **Confidence Thresholding**: Filter low-confidence predictions
4. **Feature Visualization**: Show what network learned
5. **Model Compression**: Quantization, pruning, distillation
6. **Advanced Metrics**: Accuracy, precision, recall
7. **User Accounts**: Save prediction history
8. **Database**: Store predictions and user data

## Testing Strategy

### Unit Tests
- Backend: Test preprocessing, model loading
- Frontend: Test components in isolation

### Integration Tests
- Full prediction pipeline
- API contract testing
- Error handling

### End-to-End Tests
- User workflows
- All dataset models
- Different image types

### Performance Tests
- Inference latency
- Memory usage
- Throughput
