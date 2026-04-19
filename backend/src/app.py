"""FastAPI backend for LULC Recognition System."""

import torch
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import io

from model_loader import get_model_loader
from preprocessing import get_preprocessor
from class_mappings import get_class_label
from src.explainers import generate_all_explanations


app = FastAPI(
    title="LULC Recognition API",
    description="Deep Learning Land Use & Land Cover Recognition System",
    version="1.0.0"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class ClassPrediction(BaseModel):
    class_index: int
    class_label: str
    confidence: float


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    predicted_class: str
    class_index: int
    confidence: float
    all_predictions: list[ClassPrediction]
    explainability_maps: dict
    inference_time_ms: float
    model_type: str
    image_info: dict


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    device: str
    models_available: list[str]


# Validation utilities
VALID_IMAGE_FORMATS = {"image/jpeg", "image/png", "image/jpg"}
VALID_MODEL_TYPES = {"eurosat", "mlrsnet", "patternnet"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image(file: UploadFile) -> bytes:
    """Validate and read image file."""
    print(
        f"[predict] validate_image: filename={file.filename}, "
        f"content_type={file.content_type}"
    )
    if file.content_type not in VALID_IMAGE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format. Supported: JPEG, PNG. Got: {file.content_type}"
        )
    
    # Read file content
    try:
        content = file.file.read()
        print(f"[predict] validate_image: bytes_read={len(content)}")
        if len(content) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Image too large. Max size: {MAX_IMAGE_SIZE / 1024 / 1024}MB"
            )
        return content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading image: {str(e)}")


def calculate_flops(input_shape: tuple = (1, 3, 224, 224)) -> int:
    """
    Estimate FLOPs for the SimpleCNN model.
    
    This is a simplified calculation for demonstration.
    A full calculation would require kernel size analysis.
    """
    # Approximate based on layers: ~106M FLOPs for this model
    return 106_000_000


# Routes
@app.get("/")
async def root():
    """Root endpoint for HuggingFace health checks."""
    return {"status": "ok", "message": "LULC Recognition API is running"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    loader = get_model_loader()
    return HealthResponse(
        status="healthy",
        device=str(loader.get_device()),
        models_available=list(VALID_MODEL_TYPES)
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    model_type: str = Form(...)
):
    """
    Predict LULC class for uploaded image.
    
    Args:
        file: Image file (JPEG or PNG)
        model_type: Model to use (eurosat, mlrsnet, patternnet)
    
    Returns:
        Prediction with confidence and performance metrics
    """
    print(f"[predict] request received: model_type_raw={model_type}, file={file.filename}")

    # Validate model type
    model_type = model_type.lower().strip()
    if model_type not in VALID_MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type: {model_type}. Valid types: {', '.join(VALID_MODEL_TYPES)}"
        )
    
    # Validate and read image
    image_bytes = validate_image(file)
    
    try:
        # Get preprocessor and model
        preprocessor = get_preprocessor()
        loader = get_model_loader()
        print(f"[predict] device={loader.get_device()}")
        
        # Get image info for response
        image_info = preprocessor.get_image_info(image_bytes)
        print(f"[predict] image_info={image_info}")
        
        # Preprocess image
        image_tensor = preprocessor.preprocess(image_bytes, model_type)
        image_tensor = image_tensor.to(loader.get_device())
        print(
            f"[predict] image_tensor: shape={tuple(image_tensor.shape)}, "
            f"dtype={image_tensor.dtype}, device={image_tensor.device}"
        )
        
        # Run inference with timing
        start_time = time.time()
        
        with torch.no_grad():
            model = loader.load_model(model_type)
            print(
                f"[predict] model ready: class={model.__class__.__name__}, "
                f"training={model.training}"
            )
            logits = model(image_tensor)
            print(f"[predict] logits shape={tuple(logits.shape)}")
            probabilities = torch.softmax(logits, dim=1)
            
            all_probs, all_indices = torch.sort(probabilities, descending=True, dim=1)
            
            all_predictions = []
            for i in range(all_probs.shape[1]):
                idx = all_indices[0, i].item()
                prob = float(all_probs[0, i].item())
                label = get_class_label(model_type, idx)
                all_predictions.append(ClassPrediction(
                    class_index=idx,
                    class_label=label,
                    confidence=prob
                ))

            topk = min(60, probabilities.shape[1])
            top_probs_k, top_indices_k = torch.topk(probabilities, k=topk, dim=1)
            print(
                f"[predict] top{topk}: "
                f"indices={top_indices_k[0].tolist()}, "
                f"probs={[round(float(v), 6) for v in top_probs_k[0].tolist()]}"
            )
        
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        print(f"[predict] inference_time_ms={inference_time:.3f}")
        
        # Generate explanations (we do this after inference timer to not skew metrics)
        explain_maps = generate_all_explanations(model, preprocessor, image_tensor, image_bytes, model_type)
        
        # Get prediction
        class_idx = all_predictions[0].class_index
        confidence = all_predictions[0].confidence
        class_label = all_predictions[0].class_label
        
        print(
            f"[predict] prediction: class_idx={class_idx}, "
            f"label={class_label}, confidence={confidence:.6f}"
        )
        
        return PredictionResponse(
            predicted_class=class_label,
            class_index=class_idx,
            confidence=confidence,
            all_predictions=all_predictions,
            explainability_maps=explain_maps,
            inference_time_ms=float(inference_time),
            model_type=model_type,
            image_info=image_info
        )
    
    except Exception as e:
        print(f"[predict] error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {str(e)}"
        )


@app.get("/info")
async def get_info():
    """Get system information."""
    flops = calculate_flops()
    return {
        "system": "Deep Learning LULC Recognition",
        "version": "1.0.0",
        "models": list(VALID_MODEL_TYPES),
        "architecture": "Explainable CNN",
        "parameters_approx": 400_000,
        "flops_approx": flops,
        "device": str(get_model_loader().get_device()),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
