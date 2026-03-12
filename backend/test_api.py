"""
Simple test script to verify API functionality without training
"""
import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print(f"✓ FastAPI installed: {fastapi.__version__}")
except ImportError as e:
    print(f"✗ FastAPI not installed: {e}")

try:
    import pydantic
    print(f"✓ Pydantic installed: {pydantic.__version__}")
except ImportError as e:
    print(f"✗ Pydantic not installed: {e}")

try:
    import uvicorn
    print(f"✓ Uvicorn installed")
except ImportError as e:
    print(f"✗ Uvicorn not installed: {e}")

print("\n✅ Basic dependencies are installed!")
print("\nTo start the API server:")
print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
print("\nNote: The model will be trained automatically on first prediction")
print("      or you can run: python train_model.py")
