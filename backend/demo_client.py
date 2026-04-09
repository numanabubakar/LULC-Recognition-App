"""Demo client for testing the LULC API."""

import requests
import json
from pathlib import Path
from PIL import Image
import io


def create_test_image(size=(224, 224)):
    """Create a simple test image."""
    import numpy as np
    
    # Create random RGB image
    data = np.random.randint(0, 256, (size[0], size[1], 3), dtype=np.uint8)
    img = Image.fromarray(data, 'RGB')
    return img


def save_test_image(filename="test_image.jpg"):
    """Save a test image to disk."""
    img = create_test_image()
    img.save(filename)
    return filename


def test_predict(model_type="eurosat", image_path=None):
    """Test the /predict endpoint."""
    
    # Create test image if not provided
    if image_path is None:
        image_path = save_test_image()
    
    url = "http://localhost:8000/predict"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {"model_type": model_type}
        
        print(f"\n📤 Testing /predict endpoint")
        print(f"   Model: {model_type}")
        print(f"   Image: {image_path}")
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"   Predicted: {result['predicted_class']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Inference Time: {result['inference_time_ms']:.2f}ms")
            print(f"   Class Index: {result['class_index']}")
            
            if 'all_predictions' in result:
                print("\n   Top 5 Predictions:")
                for i, pred in enumerate(result['all_predictions'][:5]):
                    print(f"      {i+1}. {pred['class_label']} ({pred['confidence']:.2%})")
            
            if 'explainability_maps' in result:
                print("\n   Visual Explanations Generated:")
                for name, b64_str in result['explainability_maps'].items():
                    print(f"      - {name}")
                    # Remove the data:image/jpeg;base64, prefix if testing saving:
                    # b64_data = b64_str.split(',')[1]
                    # with open(f"test_{name.lower().replace('+', 'p')}_map.jpg", "wb") as fh:
                    #     fh.write(base64.b64decode(b64_data))
                        
            return result
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None


def test_health():
    """Test the /health endpoint."""
    url = "http://localhost:8000/health"
    
    print("\n🏥 Testing /health endpoint")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Server is healthy!")
        print(f"   Status: {data['status']}")
        print(f"   Device: {data['device']}")
        print(f"   Models: {', '.join(data['models_available'])}")
        return data
    else:
        print(f"\n❌ Error: {response.status_code}")
        return None


def test_info():
    """Test the /info endpoint."""
    url = "http://localhost:8000/info"
    
    print("\n📋 Testing /info endpoint")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ System Information:")
        print(f"   System: {data['system']}")
        print(f"   Version: {data['version']}")
        print(f"   Architecture: {data['architecture']}")
        print(f"   Parameters: {data['parameters_approx']:,}")
        print(f"   FLOPs: {data['flops_approx']:,}")
        print(f"   Device: {data['device']}")
        print(f"   Models: {', '.join(data['models'])}")
        return data
    else:
        print(f"\n❌ Error: {response.status_code}")
        return None


def run_full_demo():
    """Run complete demo of all endpoints."""
    
    print("=" * 60)
    print("  LULC Recognition System - API Demo")
    print("=" * 60)
    
    # Check health
    if not test_health():
        print("\n⚠️  Backend is not running!")
        print("   Start it with: uv run app.py")
        return
    
    # Get system info
    test_info()
    
    # Test each model
    models = ["eurosat", "mlrsnet", "patternnet"]
    
    print("\n" + "=" * 60)
    print("  Running Predictions")
    print("=" * 60)
    
    for model in models:
        test_predict(model_type=model)
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "health":
            test_health()
        elif sys.argv[1] == "info":
            test_info()
        elif sys.argv[1] == "predict":
            model = sys.argv[2] if len(sys.argv) > 2 else "eurosat"
            image = sys.argv[3] if len(sys.argv) > 3 else None
            test_predict(model, image)
        else:
            print("Usage: python demo_client.py [health|info|predict|all] [model] [image_path]")
    else:
        run_full_demo()
