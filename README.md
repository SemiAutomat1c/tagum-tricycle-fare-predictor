# 🛺 Tricycle Fare Optimizer for Tagum City

A comprehensive web application that predicts tricycle fares in Tagum City using a Random Forest machine learning model, interactive mapping, and real-time route calculation.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Model Training](#model-training)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- 📍 **GPS Location Detection**: Automatically detects user's current location
- 🗺️ **Interactive Map**: Leaflet.js-powered map with OpenStreetMap tiles
- 🎯 **Flexible Origin Selection**: Change origin point by clicking on map
- 📌 **Destination Marking**: Click anywhere to set destination
- 🛣️ **Smart Routing**: Uses OSRM API for accurate route calculation (not straight-line distance)
- 📏 **Distance Calculation**: Automatic distance calculation along actual roads
- 🤖 **ML-Powered Prediction**: Random Forest model for accurate fare estimation
- 💰 **Real-time Fare Prediction**: Instant fare estimates based on route and conditions

### User Experience
- 📱 **Fully Responsive**: Works seamlessly on mobile, tablet, and desktop
- 🎨 **Modern UI**: Clean, intuitive interface with smooth animations
- 🚫 **Error Handling**: Comprehensive error messages for all scenarios
- ♿ **Accessible**: Keyboard navigation and screen reader friendly
- 🔄 **Easy Reset**: Quick route reset functionality

## 🛠️ Tech Stack

### Frontend
- **HTML5/CSS3**: Semantic markup and modern styling
- **Vanilla JavaScript**: No framework dependencies
- **Leaflet.js 1.9.4**: Interactive mapping library
- **OpenStreetMap**: Free, open-source map tiles
- **OSRM API**: Open Source Routing Machine for route calculation

### Backend
- **Flask 3.0.0**: Lightweight Python web framework
- **scikit-learn 1.3.2**: Machine learning library
- **pandas 2.1.4**: Data manipulation
- **joblib 1.3.2**: Model serialization
- **Flask-CORS 4.0.0**: Cross-origin resource sharing

### Deployment
- **Frontend**: Vercel (static hosting)
- **Backend**: Render.com / Railway.app / PythonAnywhere
- **Version Control**: Git & GitHub

## 📁 Project Structure

```
tricycle-fare-optimizer/
├── index.html              # Main HTML page
├── style.css               # Responsive styles
├── app.js                  # Frontend application logic
├── vercel.json             # Vercel deployment config
├── .gitignore              # Git ignore rules
├── README.md               # This file
│
├── backend/                # Flask API
│   ├── app.py              # Flask application
│   ├── model.pkl           # Trained ML model (to be added)
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render deployment config
│   ├── railway.json        # Railway deployment config
│   ├── Procfile            # Process file for deployment
│   ├── .gitignore          # Backend-specific ignores
│   └── README.md           # Backend documentation
│
└── docs/                   # Additional documentation
    ├── DEPLOYMENT.md       # Deployment guide
    ├── API.md              # API documentation
    └── TRAINING.md         # Model training guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for map tiles and routing API)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tricycle-fare-optimizer.git
cd tricycle-fare-optimizer
```

### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Add Your Model

Place your trained `model.pkl` file in the `backend/` directory:

```bash
backend/
├── app.py
├── model.pkl  ← Your model here
└── ...
```

### 4. Run Backend

```bash
# From backend directory with venv activated
python app.py
```

Backend will run on `http://localhost:5000`

### 5. Run Frontend

Open `index.html` in your web browser, or use a simple HTTP server:

```bash
# From project root
python -m http.server 8000

# Or if you have Node.js
npx serve
```

Visit `http://localhost:8000`

### 6. Configure API Endpoint

If running locally, the frontend is already configured to use `http://localhost:5000`. For production, update `app.js`:

```javascript
const CONFIG = {
    // ... other config
    backendAPI: 'https://your-backend-url.com/predict'
};
```

## 📖 Detailed Setup

### Frontend Setup

1. **No build process required**: The frontend uses vanilla JavaScript
2. **Map tiles**: Automatically loaded from OpenStreetMap CDN
3. **Routing**: Uses public OSRM API (no API key needed)
4. **Browser compatibility**: Works in all modern browsers

### Backend Setup

#### Windows

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Linux/Mac

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Verify Installation

```bash
# Test if backend is running
curl http://localhost:5000/

# Expected response:
# {"status": "online", "message": "Tricycle Fare Optimizer API", ...}
```

## 📱 Usage Guide

### Step-by-Step Instructions

1. **Open the Application**
   - Load the webpage in your browser
   - Allow location access when prompted (optional but recommended)

2. **Set Origin Point**
   - If GPS is enabled, your current location is automatically set
   - To change origin: Click "Change Origin Point" button, then click on map
   - Origin marker is **blue** and draggable

3. **Set Destination**
   - Click anywhere on the map to set your destination
   - Destination marker is **red**
   - Only one destination allowed at a time

4. **View Route**
   - Route automatically calculates after setting both points
   - Blue line shows the route along actual roads
   - Distance displays in the form (read-only)

5. **Enter Parameters**
   - **Fuel Price Range**: Current fuel price per liter
   - **Time of Day**: When you'll be traveling
   - **Weather**: Current or expected weather
   - **Vehicle Type**: Single motor or tricycle

6. **Get Prediction**
   - Click "Predict Fare" button
   - Wait for prediction (shows loading spinner)
   - Predicted fare displays in green box

7. **Reset Route**
   - Click "Reset Route" to start over
   - Origin remains, only destination is cleared

### Example Scenario

```
Origin: Gaisano Mall Tagum (your current location)
Destination: Tagum City Hall

Parameters:
- Fuel Price: ₱60-69
- Time: Rush Hour Morning
- Weather: Sunny
- Vehicle: Tricycle

Result: Predicted Fare ₱45.50
```

## 🔌 API Documentation

### Base URL
```
Local: http://localhost:5000
Production: https://your-backend-url.com
```

### Endpoints

#### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "online",
  "message": "Tricycle Fare Optimizer API",
  "version": "1.0.0"
}
```

#### Predict Fare
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "Distance_km": 5.23,
  "Fuel_Price": "60-69",
  "Time_of_Day": "Rush Hour Morning",
  "Weather": "Sunny",
  "Vehicle_Type": "Tricycle"
}
```

**Valid Parameter Values:**

| Parameter | Valid Values |
|-----------|--------------|
| Distance_km | Float > 0 |
| Fuel_Price | "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100&up" |
| Time_of_Day | "Rush Hour Morning", "Off-Peak", "Rush Hour Evening" |
| Weather | "Sunny", "Rainy" |
| Vehicle_Type | "Single Motor", "Tricycle" |

**Success Response (200):**
```json
{
  "predicted_fare": 45.50,
  "input": { ... }
}
```

**Error Response (400):**
```json
{
  "error": "Missing required field: Distance_km"
}
```

### Testing with cURL

```bash
# Health check
curl http://localhost:5000/

# Prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"Distance_km": 5.5, "Fuel_Price": "60-69", "Time_of_Day": "Rush Hour Morning", "Weather": "Sunny", "Vehicle_Type": "Tricycle"}'
```

## 🎓 Model Training

### Dataset Requirements

Your CSV dataset must have exactly these columns:

```csv
Distance_km,Fuel_Price,Time_of_Day,Weather,Vehicle_Type,Actual_Fare_PHP
5.2,60-69,Rush Hour Morning,Sunny,Tricycle,45.00
3.1,40-49,Off-Peak,Rainy,Single Motor,28.50
...
```

### Training Script

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load dataset
df = pd.read_csv('tricycle_fare_data.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Encode categorical variables
label_encoders = {}
categorical_columns = ['Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']

for col in categorical_columns:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"{col} encoding: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Prepare features and target
X = df[['Distance_km', 'Fuel_Price_encoded', 'Time_of_Day_encoded', 
        'Weather_encoded', 'Vehicle_Type_encoded']]
y = df['Actual_Fare_PHP']

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

print("\nTraining model...")
model.fit(X_train, y_train)

# Evaluate model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"\n=== Model Performance ===")
print(f"Training R² Score: {train_score:.4f}")
print(f"Test R² Score: {test_score:.4f}")
print(f"Mean Absolute Error: ₱{mae:.2f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': ['Distance_km', 'Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type'],
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n=== Feature Importance ===")
print(feature_importance)

# Save model
joblib.dump(model, 'backend/model.pkl')
print("\n✅ Model saved as 'backend/model.pkl'")

# Save encoders (optional, for reference)
joblib.dump(label_encoders, 'backend/label_encoders.pkl')
print("✅ Encoders saved as 'backend/label_encoders.pkl'")
```

### Important Notes

⚠️ **Model Encoding**: The current backend expects the model to handle string categorical values directly. If your model requires encoded values, modify `backend/app.py` to include encoding logic using the saved `label_encoders.pkl`.

## 🌐 Deployment

### Frontend Deployment (Vercel)

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

3. **Deploy via Vercel Dashboard**:
   - Visit [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Deploy automatically

4. **Or deploy via CLI**:
   ```bash
   vercel
   ```

5. **Configure Environment Variable**:
   - In Vercel dashboard, add environment variable:
   - `BACKEND_API_URL` = your backend URL

### Backend Deployment

#### Option 1: Render.com (Recommended)

1. **Create Account**: [render.com](https://render.com)

2. **New Web Service**:
   - Connect GitHub repository
   - Select `backend` directory
   - Use `render.yaml` configuration

3. **Add Model File**:
   - Upload `model.pkl` through dashboard
   - Or commit it to repository (if < 100MB)

4. **Deploy**: Automatic deployment from GitHub

#### Option 2: Railway.app

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

3. **Add Model**: Upload through dashboard

#### Option 3: PythonAnywhere

See `backend/README.md` for detailed instructions.

### Post-Deployment

1. **Update Frontend Config**:
   ```javascript
   // In app.js
   const CONFIG = {
       backendAPI: 'https://your-backend.onrender.com/predict'
   };
   ```

2. **Configure CORS** in `backend/app.py`:
   ```python
   CORS(app, origins=[
       'https://your-vercel-app.vercel.app'
   ])
   ```

3. **Test Deployment**:
   ```bash
   curl https://your-backend.onrender.com/health
   ```

## 🔧 Troubleshooting

### Common Issues

#### 1. Location Not Detected
- **Solution**: Check browser permissions, use "Change Origin" button
- **Firefox**: about:preferences > Privacy & Security > Permissions > Location
- **Chrome**: Settings > Privacy and security > Site settings > Location

#### 2. Route Not Calculating
- **Causes**: 
  - OSRM API down (rare)
  - No route available between points
  - Points too far apart
- **Solution**: Try different locations, check console for errors

#### 3. Prediction Fails
- **Error**: "Cannot connect to prediction server"
  - Backend not running
  - Incorrect API URL in `app.js`
  - CORS issues
- **Solution**: 
  ```bash
  # Check backend is running
  curl http://localhost:5000/health
  
  # Check browser console for errors
  # Verify CONFIG.backendAPI in app.js
  ```

#### 4. Model Not Loading
- **Error**: "Model not available"
- **Solution**:
  ```bash
  cd backend
  ls model.pkl  # Should exist
  python app.py  # Check logs
  ```

#### 5. CORS Errors
- **Error**: "Access-Control-Allow-Origin"
- **Solution**: Update `backend/app.py`:
  ```python
  CORS(app, origins=['http://localhost:8000'])
  ```

### Debug Mode

Enable detailed logging:

```python
# In backend/app.py
app.run(debug=True)  # Shows detailed errors
```

```javascript
// In app.js, check browser console
console.log('Debug info')
```

## ⚠️ Known Limitations

1. **Route Availability**: OSRM may not have routes for very remote areas
2. **Model Accuracy**: Depends on training data quality and coverage
3. **Free API Limits**: OSRM public API has rate limits (usually sufficient)
4. **Offline Use**: Requires internet for map tiles and routing
5. **Model Size**: Large models may slow down backend startup
6. **Browser Support**: Requires modern browser with geolocation API

## 🚀 Future Enhancements

### Planned Features
- [ ] Multiple waypoint support
- [ ] Save favorite locations
- [ ] Recent predictions history (localStorage)
- [ ] Export predictions to CSV/PDF
- [ ] Dark mode toggle
- [ ] Multi-language support (English/Tagalog)
- [ ] Voice input for destination
- [ ] Share route link functionality

### Advanced Features
- [ ] Real-time fare updates based on actual traffic
- [ ] Driver-side companion app
- [ ] Booking system integration
- [ ] Payment gateway integration
- [ ] User accounts and history
- [ ] Admin dashboard for analytics
- [ ] Mobile app (React Native/Flutter)

### ML Improvements
- [ ] Model retraining pipeline
- [ ] A/B testing for model versions
- [ ] Confidence intervals for predictions
- [ ] Anomaly detection for unusual fares
- [ ] Time series forecasting for fuel prices

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write meaningful commit messages
- Add tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - Initial work

## 🙏 Acknowledgments

- OpenStreetMap contributors for map data
- OSRM project for routing engine
- Leaflet.js for mapping library
- scikit-learn community
- Flask framework developers

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: your.email@example.com
- Documentation: See `docs/` folder

## 📸 Screenshots

<!-- Add screenshots here after deployment -->

## 🎥 Demo Video

<!-- Add demo video link here -->

---

**Built with ❤️ for Tagum City**
