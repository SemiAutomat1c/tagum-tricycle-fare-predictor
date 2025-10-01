"""
Vercel Serverless Function for Tricycle Fare Prediction
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Load model
model_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model.pkl')
model = None

try:
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# Valid categorical values
VALID_VALUES = {
    'Fuel_Price': ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100&up'],
    'Time_of_Day': ['Rush Hour Morning', 'Off-Peak', 'Rush Hour Evening'],
    'Weather': ['Sunny', 'Rainy'],
    'Vehicle_Type': ['Single Motor', 'Tricycle']
}

def validate_input_data(data):
    """Validate incoming prediction request data"""
    required_fields = ['Distance_km', 'Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    try:
        distance = float(data['Distance_km'])
        if distance <= 0:
            return False, "Distance must be greater than 0"
        if distance > 1000:
            return False, "Distance seems unrealistic (> 1000 km)"
    except (ValueError, TypeError):
        return False, "Distance_km must be a valid number"
    
    for field, valid_values in VALID_VALUES.items():
        if data[field] not in valid_values:
            return False, f"Invalid {field}: '{data[field]}'. Must be one of: {', '.join(valid_values)}"
    
    return True, None

def prepare_input_dataframe(data):
    """Convert input data to pandas DataFrame with encoded features"""
    df = pd.DataFrame([data])
    
    df['Distance_km'] = df['Distance_km'].astype(float)
    
    # Encoding mappings (must match training data)
    encodings = {
        'Fuel_Price': {'100&up': 0, '20-29': 1, '30-39': 2, '40-49': 3, '50-59': 4, '60-69': 5, '70-79': 6, '80-89': 7, '90-99': 8},
        'Time_of_Day': {'Off-Peak': 0, 'Rush Hour Evening': 1, 'Rush Hour Morning': 2},
        'Weather': {'Rainy': 0, 'Sunny': 1},
        'Vehicle_Type': {'Single Motor': 0, 'Tricycle': 1}
    }
    
    categorical_columns = ['Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']
    
    for col in categorical_columns:
        df[col + '_encoded'] = df[col].map(encodings[col])
    
    encoded_columns = ['Distance_km'] + [col + '_encoded' for col in categorical_columns]
    df = df[encoded_columns]
    
    return df

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict tricycle fare"""
    try:
        if model is None:
            return jsonify({'error': 'Model not available'}), 500
        
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        is_valid, error_message = validate_input_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        input_df = prepare_input_dataframe(data)
        prediction = model.predict(input_df)
        predicted_fare = round(float(prediction[0]), 2)
        
        return jsonify({
            'predicted_fare': predicted_fare,
            'input': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error during prediction',
            'details': str(e)
        }), 500

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

