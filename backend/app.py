"""
Tricycle Fare Optimizer - Flask Backend API
============================================
This Flask application provides a REST API endpoint for predicting tricycle fares
using a pre-trained Random Forest machine learning model.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (allows requests from Vercel frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variable to store the loaded model
model = None

# Expected column order for the model
EXPECTED_COLUMNS = [
    'Distance_km',
    'Fuel_Price',
    'Time_of_Day',
    'Weather',
    'Vehicle_Type'
]

# Valid categorical values (must match training data encoding)
VALID_VALUES = {
    'Fuel_Price': ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100&up'],
    'Time_of_Day': ['Rush Hour Morning', 'Off-Peak', 'Rush Hour Evening'],
    'Weather': ['Sunny', 'Rainy'],
    'Vehicle_Type': ['Single Motor', 'Tricycle']
}


def load_model():
    """
    Load the pre-trained Random Forest model from disk
    Returns: Loaded model object or None if loading fails
    """
    global model
    
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        logger.error("Please ensure 'model.pkl' is in the backend directory")
        return None
    
    try:
        model = joblib.load(model_path)
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return None


def validate_input_data(data):
    """
    Validate incoming prediction request data
    
    Args:
        data (dict): Request data from client
        
    Returns:
        tuple: (is_valid (bool), error_message (str or None))
    """
    # Check if all required fields are present
    for column in EXPECTED_COLUMNS:
        if column not in data:
            return False, f"Missing required field: {column}"
    
    # Validate Distance_km
    try:
        distance = float(data['Distance_km'])
        if distance <= 0:
            return False, "Distance must be greater than 0"
        if distance > 1000:  # Sanity check
            return False, "Distance seems unrealistic (> 1000 km)"
    except (ValueError, TypeError):
        return False, "Distance_km must be a valid number"
    
    # Validate categorical fields
    for field, valid_values in VALID_VALUES.items():
        if data[field] not in valid_values:
            return False, f"Invalid {field}: '{data[field]}'. Must be one of: {', '.join(valid_values)}"
    
    return True, None


def prepare_input_dataframe(data):
    """
    Convert input data to pandas DataFrame with correct format
    
    Args:
        data (dict): Validated input data
        
    Returns:
        pd.DataFrame: Formatted DataFrame ready for model prediction
    """
    # Create DataFrame with correct column order
    df = pd.DataFrame([data], columns=EXPECTED_COLUMNS)
    
    # Ensure Distance_km is float
    df['Distance_km'] = df['Distance_km'].astype(float)
    
    # Encode categorical variables to match training format
    # The model was trained with encoded column names
    categorical_columns = ['Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']
    
    # Mapping for categorical encoding (must match training data)
    encodings = {
        'Fuel_Price': {'100&up': 0, '20-29': 1, '30-39': 2, '40-49': 3, '50-59': 4, '60-69': 5, '70-79': 6, '80-89': 7, '90-99': 8},
        'Time_of_Day': {'Off-Peak': 0, 'Rush Hour Evening': 1, 'Rush Hour Morning': 2},
        'Weather': {'Rainy': 0, 'Sunny': 1},
        'Vehicle_Type': {'Single Motor': 0, 'Tricycle': 1}
    }
    
    # Create encoded columns
    for col in categorical_columns:
        df[col + '_encoded'] = df[col].map(encodings[col])
    
    # Select only the columns the model expects (Distance_km + encoded columns)
    encoded_columns = ['Distance_km'] + [col + '_encoded' for col in categorical_columns]
    df = df[encoded_columns]
    
    return df


@app.route('/')
def home():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'online',
        'message': 'Tricycle Fare Optimizer API',
        'version': '1.0.0',
        'endpoints': {
            '/predict': 'POST - Predict tricycle fare'
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict tricycle fare based on input parameters
    
    Expected JSON input:
    {
        "Distance_km": float,
        "Fuel_Price": string,
        "Time_of_Day": string,
        "Weather": string,
        "Vehicle_Type": string
    }
    
    Returns JSON:
    {
        "predicted_fare": float
    }
    """
    try:
        # Check if model is loaded
        if model is None:
            logger.error("Model not loaded")
            return jsonify({
                'error': 'Model not available. Please contact administrator.'
            }), 500
        
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        logger.info(f"Received prediction request: {data}")
        
        # Validate input data
        is_valid, error_message = validate_input_data(data)
        if not is_valid:
            logger.warning(f"Validation failed: {error_message}")
            return jsonify({
                'error': error_message
            }), 400
        
        # Prepare data for prediction
        input_df = prepare_input_dataframe(data)
        logger.info(f"Prepared input DataFrame:\n{input_df}")
        
        # Make prediction
        prediction = model.predict(input_df)
        predicted_fare = float(prediction[0])
        
        # Round to 2 decimal places
        predicted_fare = round(predicted_fare, 2)
        
        logger.info(f"Prediction successful: ₱{predicted_fare}")
        
        return jsonify({
            'predicted_fare': predicted_fare,
            'input': data
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error during prediction',
            'details': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Detailed health check endpoint
    """
    model_status = 'loaded' if model is not None else 'not loaded'
    
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'api_version': '1.0.0'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500


# Application entry point
if __name__ == '__main__':
    logger.info("Starting Tricycle Fare Optimizer API...")
    
    # Load the model
    if load_model() is None:
        logger.warning("API starting without model loaded")
        logger.warning("Prediction requests will fail until model is available")
    
    # Run the Flask app
    # For production, use a proper WSGI server like Gunicorn
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Set to False in production
    )
