# Quick Start Guide

Get the Tricycle Fare Optimizer running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Modern web browser
- Internet connection

## Windows Users

### 1. Run Setup Script
```bash
setup.bat
```

This will:
- Check Python installation
- Create virtual environment
- Install all dependencies
- Check for model file

### 2. Generate Sample Data (if needed)
```bash
py sample_data_generator.py
```

### 3. Train Model (if needed)
```bash
py train_model.py
```

### 4. Start Backend
```bash
cd backend
venv\Scripts\activate
py app.py
```

### 5. Open Frontend
- Double-click `index.html`
- Or open it in your browser

## Linux/Mac Users

### 1. Make Setup Script Executable
```bash
chmod +x setup.sh
```

### 2. Run Setup Script
```bash
./setup.sh
```

### 3. Generate Sample Data (if needed)
```bash
python3 sample_data_generator.py
```

### 4. Train Model (if needed)
```bash
python3 train_model.py
```

### 5. Start Backend
```bash
cd backend
source venv/bin/activate
python3 app.py
```

### 6. Open Frontend
```bash
# Option 1: Direct file
open index.html  # Mac
xdg-open index.html  # Linux

# Option 2: HTTP Server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Manual Setup (All Platforms)

If the automated scripts don't work:

### Backend Setup
```bash
cd backend
python -m venv venv

# Activate venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
python app.py
```

### Frontend
Just open `index.html` in your browser!

## Testing

### Test Backend API
```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "status": "online",
  "message": "Tricycle Fare Optimizer API"
}
```

### Test Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"Distance_km\": 5.0, \"Fuel_Price\": \"60-69\", \"Time_of_Day\": \"Off-Peak\", \"Weather\": \"Sunny\", \"Vehicle_Type\": \"Tricycle\"}"
```

## Troubleshooting

### "Python not found"
- Install Python from [python.org](https://python.org)
- Make sure to check "Add to PATH" during installation

### "pip not found"
```bash
python -m ensurepip --upgrade
```

### "Port 5000 already in use"
- Close other applications using port 5000
- Or change port in `backend/app.py`:
  ```python
  app.run(port=5001)  # Use different port
  ```

### "Model not found"
- Run `sample_data_generator.py` first
- Then run `train_model.py`
- Verify `backend/model.pkl` exists

### CORS Errors
- Make sure backend is running
- Check `CONFIG.backendAPI` in `app.js`
- For local testing, use `http://localhost:5000/predict`

## Default Credentials / Settings

- Backend URL: `http://localhost:5000`
- Frontend: Open `index.html` directly
- Map Center: Tagum City (7.4474°N, 125.8072°E)
- Default Zoom: 14

## What's Next?

1. **Use Real Data**: Replace sample data with actual fare data
2. **Retrain Model**: Run `train_model.py` with your data
3. **Customize UI**: Edit `style.css` for your branding
4. **Deploy**: See README.md for deployment instructions

## Getting Help

- Full documentation: See `README.md`
- Backend API docs: See `backend/README.md`
- Issues: Check the troubleshooting section above

---

**Ready to predict fares!** 🚀
