"""Debug script to check if model file exists"""
import os
import sys

print("="*50)
print("Model File Debug Check")
print("="*50)

# Current directory
print(f"\nCurrent directory: {os.getcwd()}")

# List files in current directory
print(f"\nFiles in current directory:")
for f in os.listdir('.'):
    print(f"  - {f}")

# Check for model.pkl
model_path = 'model.pkl'
print(f"\nChecking for {model_path}:")
print(f"  Exists: {os.path.exists(model_path)}")
if os.path.exists(model_path):
    print(f"  Size: {os.path.getsize(model_path)} bytes")
    print(f"  Abs path: {os.path.abspath(model_path)}")

# Try loading
try:
    import joblib
    model = joblib.load(model_path)
    print(f"\n✅ Model loaded successfully!")
    print(f"  Model type: {type(model)}")
except Exception as e:
    print(f"\n❌ Error loading model: {e}")

print("="*50)

