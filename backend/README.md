# Tricycle Fare Optimizer - Backend API

Flask-based REST API for predicting tricycle fares using a Random Forest machine learning model.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A trained Random Forest model saved as `model.pkl`

## Local Development Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Trained Model

Place your trained Random Forest model file in the backend directory:
```
backend/
├── app.py
├── model.pkl  ← Your model file here
├── requirements.txt
└── README.md
```

### 5. Run the Development Server

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "message": "Tricycle Fare Optimizer API",
  "version": "1.0.0"
}
```

### `POST /predict`
Predict tricycle fare based on route and conditions.

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

**Valid Values:**
- `Fuel_Price`: "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100&up"
- `Time_of_Day`: "Rush Hour Morning", "Off-Peak", "Rush Hour Evening"
- `Weather`: "Sunny", "Rainy"
- `Vehicle_Type`: "Single Motor", "Tricycle"

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

### `GET /health`
Detailed health check with model status.

**Response:**
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "api_version": "1.0.0"
}
```

## Testing with cURL

### Test Health Check
```bash
curl http://localhost:5000/
```

### Test Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"Distance_km\": 5.5, \"Fuel_Price\": \"60-69\", \"Time_of_Day\": \"Rush Hour Morning\", \"Weather\": \"Sunny\", \"Vehicle_Type\": \"Tricycle\"}"
```

## Training and Saving the Model

If you need to train a new model, use this Python script:

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset
df = pd.read_csv('tricycle_fare_data.csv')

# Encode categorical variables
label_encoders = {}
categorical_columns = ['Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Prepare features and target
X = df.drop('Actual_Fare_PHP', axis=1)
y = df['Actual_Fare_PHP']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'model.pkl')
print("Model saved as model.pkl")

# Test accuracy
score = model.score(X_test, y_test)
print(f"Model R² Score: {score:.4f}")
```

**Important:** The API expects the model to accept categorical values as strings (not encoded). If your model uses encoded values, you'll need to modify the `prepare_input_dataframe` function in `app.py` to include encoding logic.

## Deployment Options

### Option 1: Render.com (Recommended)

1. Create a `render.yaml` file:
```yaml
services:
  - type: web
    name: tricycle-fare-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. Push to GitHub
3. Connect repository to Render.com
4. Deploy automatically

### Option 2: Railway.app

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add `model.pkl` through Railway dashboard

### Option 3: PythonAnywhere

1. Upload files through web interface
2. Create virtual environment
3. Configure WSGI file:
```python
import sys
path = '/home/yourusername/backend'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

4. Reload web app

## CORS Configuration

For production, update CORS settings in `app.py`:

```python
# Replace this:
CORS(app)

# With this:
CORS(app, origins=[
    'https://your-vercel-app.vercel.app',
    'https://your-custom-domain.com'
])
```

## Environment Variables

For production deployment, set these environment variables:

- `FLASK_ENV=production`
- `MODEL_PATH=/path/to/model.pkl` (optional, defaults to ./model.pkl)

## Troubleshooting

### Model Not Loading
- Ensure `model.pkl` is in the backend directory
- Check file permissions
- Verify scikit-learn version compatibility

### CORS Errors
- Update CORS configuration with your frontend URL
- Ensure backend is running before making requests

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## Production Considerations

1. **Use Gunicorn** instead of Flask development server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set Debug to False** in `app.py`

3. **Add Rate Limiting** to prevent abuse:
   ```bash
   pip install flask-limiter
   ```

4. **Use Environment Variables** for sensitive configuration

5. **Implement Logging** to file for production debugging

6. **Add Request Validation** middleware

7. **Set up Health Monitoring** with tools like UptimeRobot

## License

MIT License - See main project README for details
