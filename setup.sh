#!/bin/bash
# Setup script for Tricycle Fare Optimizer (Linux/Mac)

echo "========================================"
echo "Tricycle Fare Optimizer - Setup"
echo "========================================"
echo ""

# Check Python installation
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi
python3 --version
echo ""

# Navigate to backend directory
echo "[2/5] Setting up backend..."
cd backend

# Create virtual environment
echo "[3/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi
echo ""

# Activate virtual environment and install dependencies
echo "[4/5] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo ""

# Check for model file
echo "[5/5] Checking for model file..."
if [ -f "model.pkl" ]; then
    echo "Model file found: model.pkl"
else
    echo "WARNING: model.pkl not found!"
    echo ""
    echo "You need to train and add your model file:"
    echo "1. Generate sample data: python3 ../sample_data_generator.py"
    echo "2. Train model: python3 ../train_model.py"
    echo "3. Or add your own model.pkl to the backend folder"
fi
echo ""

cd ..

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. If you don't have a model, run: python3 sample_data_generator.py"
echo "2. Then run: python3 train_model.py"
echo "3. Start backend: cd backend && source venv/bin/activate && python3 app.py"
echo "4. Open index.html in your browser"
echo ""
