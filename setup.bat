@echo off
REM Setup script for Tricycle Fare Optimizer (Windows)

echo ========================================
echo Tricycle Fare Optimizer - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
py --version
echo.

REM Navigate to backend directory
echo [2/5] Setting up backend...
cd backend

REM Create virtual environment
echo [3/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists.
) else (
    py -m venv venv
    echo Virtual environment created.
)
echo.

REM Activate virtual environment and install dependencies
echo [4/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Check for model file
echo [5/5] Checking for model file...
if exist model.pkl (
    echo Model file found: model.pkl
) else (
    echo WARNING: model.pkl not found!
    echo.
    echo You need to train and add your model file:
    echo 1. Generate sample data: py ..\sample_data_generator.py
    echo 2. Train model: py ..\train_model.py
    echo 3. Or add your own model.pkl to the backend folder
)
echo.

cd ..

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. If you don't have a model, run: py sample_data_generator.py
echo 2. Then run: py train_model.py
echo 3. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& py app.py
echo 4. Open index.html in your browser
echo.
pause
