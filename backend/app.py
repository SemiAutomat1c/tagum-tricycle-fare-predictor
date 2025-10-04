"""
Tricycle Fare Optimizer - Flask Backend API (Updated for New Model)
===================================================================
This Flask application provides a REST API endpoint for predicting tricycle fares
using the new trained Random Forest model with preprocessor and scaler.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (allows requests from frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variables to store the loaded pipeline components
model = None
preprocessor = None
scaler = None
metadata = None

# Expected column order for the input
EXPECTED_COLUMNS = [
    'Distance_km',
    'Fuel_Price',
    'Time_of_Day',
    'Weather',
    'Vehicle_Type'
]

# Valid categorical values (updated for new dataset with ₱ symbol)
VALID_VALUES = {
    'Fuel_Price': ['₱20-29', '₱30-39', '₱40-49', '₱50-59', '₱60-69', '₱70-79', '₱80-89', '₱90-99', '₱100 & up'],
    'Time_of_Day': ['Rush Hour Morning', 'Off-Peak', 'Rush Hour Evening'],
    'Weather': ['Sunny', 'Rainy'],
    'Vehicle_Type': ['Single Motor', 'Tricycle']
}


def load_pipeline():
    """
    Load all pipeline components: model, preprocessor, scaler, and metadata
    Returns: True if successful, False otherwise
    """
    global model, preprocessor, scaler, metadata
    
    base_dir = os.path.dirname(__file__)
    
    # Define paths
    model_path = os.path.join(base_dir, 'model.pkl')
    preprocessor_path = os.path.join(base_dir, 'preprocessor.pkl')
    scaler_path = os.path.join(base_dir, 'scaler.pkl')
    metadata_path = os.path.join(base_dir, 'model_metadata.pkl')
    
    # Check if all files exist
    required_files = {
        'Model': model_path,
        'Preprocessor': preprocessor_path,
        'Scaler': scaler_path,
        'Metadata': metadata_path
    }
    
    missing_files = []
    for name, path in required_files.items():
        if not os.path.exists(path):
            logger.error(f"{name} file not found at {path}")
            missing_files.append(name)
    
    if missing_files:
        logger.error(f"Missing files: {', '.join(missing_files)}")
        logger.error("Please run 'py train_tagum_model.py' first to generate the model files")
        return False
    
    try:
        # Load all components
        model = joblib.load(model_path)
        logger.info("✅ Model loaded successfully")
        
        preprocessor = joblib.load(preprocessor_path)
        logger.info("✅ Preprocessor loaded successfully")
        
        scaler = joblib.load(scaler_path)
        logger.info("✅ Scaler loaded successfully")
        
        metadata = joblib.load(metadata_path)
        logger.info("✅ Metadata loaded successfully")
        logger.info(f"   Model R² Score: {metadata['r2']:.4f}")
        logger.info(f"   Model MAE: ₱{metadata['mae']:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading pipeline components: {str(e)}")
        return False


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
        if distance > 100:  # Sanity check for Tagum City
            return False, "Distance seems unrealistic (> 100 km for Tagum City)"
    except (ValueError, TypeError):
        return False, "Distance_km must be a valid number"
    
    # Validate categorical fields
    for field, valid_values in VALID_VALUES.items():
        if data[field] not in valid_values:
            return False, f"Invalid {field}: '{data[field]}'. Must be one of: {', '.join(valid_values)}"
    
    return True, None


def prepare_and_predict(data):
    """
    Prepare input data and make prediction using the full pipeline
    
    Args:
        data (dict): Validated input data
        
    Returns:
        float: Predicted fare
    """
    # Create DataFrame with correct column order
    df = pd.DataFrame([data], columns=EXPECTED_COLUMNS)
    
    # Ensure Distance_km is float
    df['Distance_km'] = df['Distance_km'].astype(float)
    
    logger.info(f"Input DataFrame:\n{df}")
    
    # Step 1: Apply preprocessor (encoding)
    X_processed = preprocessor.transform(df)
    logger.info(f"After preprocessing: shape = {X_processed.shape}")
    
    # Step 2: Apply scaler
    X_scaled = scaler.transform(X_processed)
    logger.info(f"After scaling: shape = {X_scaled.shape}")
    
    # Step 3: Make prediction
    prediction = model.predict(X_scaled)
    predicted_fare = float(prediction[0])
    
    return predicted_fare


@app.route('/')
def home():
    """
    Health check endpoint
    """
    model_info = {
        'r2_score': f"{metadata['r2']:.4f}" if metadata else 'N/A',
        'mae': f"₱{metadata['mae']:.2f}" if metadata else 'N/A'
    }
    
    return jsonify({
        'status': 'online',
        'message': 'Tagum Tricycle Fare Optimizer API',
        'version': '2.0.0',
        'model_info': model_info,
        'endpoints': {
            '/predict': 'POST - Predict tricycle fare',
            '/health': 'GET - Detailed health check'
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict tricycle fare based on input parameters
    
    Expected JSON input:
    {
        "Distance_km": float,
        "Fuel_Price": string (with ₱ symbol),
        "Time_of_Day": string,
        "Weather": string,
        "Vehicle_Type": string
    }
    
    Returns JSON:
    {
        "predicted_fare": float,
        "input": dict
    }
    """
    try:
        # Check if pipeline is loaded
        if model is None or preprocessor is None or scaler is None:
            logger.error("Pipeline components not loaded")
            return jsonify({
                'error': 'Model pipeline not available. Please contact administrator.'
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
                'error': error_message,
                'valid_fuel_prices': VALID_VALUES['Fuel_Price']
            }), 400
        
        # Make prediction using the full pipeline
        predicted_fare = prepare_and_predict(data)
        
        # Round to 2 decimal places
        predicted_fare = round(predicted_fare, 2)
        
        # Ensure non-negative fare
        predicted_fare = max(0, predicted_fare)
        
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
    pipeline_status = {
        'model': 'loaded' if model is not None else 'not loaded',
        'preprocessor': 'loaded' if preprocessor is not None else 'not loaded',
        'scaler': 'loaded' if scaler is not None else 'not loaded',
        'metadata': 'loaded' if metadata is not None else 'not loaded'
    }
    
    model_metrics = {}
    if metadata:
        model_metrics = {
            'r2_score': metadata['r2'],
            'mae': metadata['mae'],
            'mse': metadata['mse'],
            'training_samples': metadata['n_samples_train'],
            'test_samples': metadata['n_samples_test']
        }
    
    return jsonify({
        'status': 'healthy',
        'pipeline_status': pipeline_status,
        'model_metrics': model_metrics,
        'api_version': '2.0.0'
    }), 200


@app.route('/valid-values', methods=['GET'])
def valid_values():
    """
    Get valid values for categorical inputs
    """
    return jsonify({
        'valid_values': VALID_VALUES
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation',
        'available_endpoints': ['/', '/predict', '/health', '/valid-values']
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


# Load pipeline on module import
logger.info("="*60)
logger.info("Tagum Tricycle Fare Optimizer API - Module Loading")
logger.info("="*60)
logger.info(f"Current directory: {os.getcwd()}")
logger.info("Attempting to load pipeline components...")

if load_pipeline():
    logger.info("="*60)
    logger.info("SUCCESS: All pipeline components loaded!")
    logger.info("="*60)
else:
    logger.error("="*60)
    logger.error("CRITICAL: Pipeline failed to load!")
    logger.error("="*60)

# Application entry point
if __name__ == '__main__':
    logger.info("Starting Tagum Tricycle Fare Optimizer API...")
    logger.info(f"Model R² Score: {metadata['r2']:.4f}" if metadata else "Model not loaded")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Set to False in production
    )

