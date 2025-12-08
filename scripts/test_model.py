"""
Test your trained model with a single image
Run: python scripts/test_model. py
"""

import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import json
from pathlib import Path

def test_model(model_path, image_path):
    """
    Test the model with a single image
    
    Args:
        model_path: Path to your trained model (e.g., 'models/coffee-roast-v1/final_model')
        image_path: Path to test image
    """
    
    print("="*60)
    print("🧪 TESTING YOUR MODEL")
    print("="*60)
    
    # Check if model exists
    model_path = Path(model_path)
    if not model_path.exists():
        print(f"❌ Model not found at: {model_path}")
        print("\nDid you run training? Try: python scripts/train_model.py")
        return
    
    print(f"\n📂 Loading model from: {model_path}")
    
    # Load model and processor
    try:
        processor = AutoImageProcessor.from_pretrained(str(model_path))
        model = AutoModelForImageClassification. from_pretrained(str(model_path))
        model.eval()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Check device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"🖥️  Using device: {device}")
    
    # Load and display image info
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"\n❌ Image not found: {image_path}")
        return
    
    print(f"\n📸 Loading image: {image_path}")
    image = Image.open(image_path).convert('RGB')
    print(f"   Size: {image.size}")
    print(f"   Format: {image.format}")
    
    # Preprocess
    print("\n🔄 Processing image...")
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Predict
    print("🤖 Making prediction...")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional. softmax(logits, dim=-1)[0]
    
    # Get results
    predicted_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_idx]
    confidence = probabilities[predicted_idx].item()
    
    # Display results
    print("\n" + "="*60)
    print("🎯 PREDICTION RESULTS")
    print("="*60)
    print(f"\n🏆 Predicted Roast: {predicted_label. upper(). replace('_', ' ')}")
    print(f"📊 Confidence: {confidence:. 1%}")
    print(f"🎲 Roast Level: {predicted_idx}")
    
    print("\n📈 All Probabilities:")
    print("-"*60)
    
    # Sort by probability
    sorted_probs = sorted(
        [(model.config.id2label[i], probabilities[i].item()) 
         for i in range(len(probabilities))],
        key=lambda x: x[1],
        reverse=True
    )
    
    for label, prob in sorted_probs:
        bar_length = int(prob * 40)
        bar = "█" * bar_length
        print(f"{label:15s} {prob:6.1%} {bar}")
    
    print("="*60)
    print("✅ Test complete!")
    print("="*60)
    
    return {
        'predicted_roast': predicted_label,
        'confidence': confidence,
        'all_probabilities': {label: prob for label, prob in sorted_probs}
    }

if __name__ == "__main__":
    import sys
    
    # Default paths
    model_path = "models/coffee-roast-v1/final_model"
    
    # Try to find a test image
    test_image = None
    possible_paths = [
        "uploads",  # Check uploads folder first
        "data/processed/test",
        "data/processed/val",
        "data/raw/medium"
    ]
    
    for path in possible_paths:
        path = Path(path)
        if path.exists():
            images = list(path.glob("*.jpg")) + list(path.glob("*.png"))
            if images:
                test_image = str(images[0])
                break
    
    if test_image is None:
        print("❌ No test image found!")
        print("\nUsage: python scripts/test_model.py [model_path] [image_path]")
        print(f"\nExample: python scripts/test_model.py {model_path} uploads/IMG-20251114-WA0007.jpg")
        sys.exit(1)
    
    # Allow command line arguments
    if len(sys. argv) > 1:
        model_path = sys.argv[1]
    if len(sys.argv) > 2:
        test_image = sys.argv[2]
    
    print(f"Using model: {model_path}")
    print(f"Using image: {test_image}")
    print()
    
    test_model(model_path, test_image)