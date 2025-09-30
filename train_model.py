"""
Tricycle Fare Prediction Model Training Script
==============================================
This script trains a Random Forest model for predicting tricycle fares
based on distance, fuel price, time of day, weather, and vehicle type.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def load_data(filepath):
    """
    Load and validate the dataset
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    print(f"Loading data from {filepath}...")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Validate required columns
    required_columns = [
        'Distance_km',
        'Fuel_Price',
        'Time_of_Day',
        'Weather',
        'Vehicle_Type',
        'Actual_Fare_PHP'
    ]
    
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    print(f"✅ Dataset loaded successfully")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {df.columns.tolist()}")
    
    return df


def preprocess_data(df):
    """
    Preprocess the dataset: handle missing values, encode categories
    
    Args:
        df (pd.DataFrame): Raw dataset
        
    Returns:
        tuple: (X, y, label_encoders)
    """
    print("\nPreprocessing data...")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print(f"⚠️  Missing values found:")
        print(missing[missing > 0])
        df = df.dropna()
        print(f"   Dropped {len(df)} rows with missing values")
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['Fuel_Price', 'Time_of_Day', 'Weather', 'Vehicle_Type']
    
    df_encoded = df.copy()
    
    for col in categorical_columns:
        le = LabelEncoder()
        df_encoded[col + '_encoded'] = le.fit_transform(df[col])
        label_encoders[col] = le
        
        # Print encoding mapping
        print(f"\n{col} encoding:")
        for class_name, encoded_value in zip(le.classes_, le.transform(le.classes_)):
            print(f"   {class_name} -> {encoded_value}")
    
    # Prepare features (X) and target (y)
    feature_columns = ['Distance_km'] + [col + '_encoded' for col in categorical_columns]
    X = df_encoded[feature_columns]
    y = df_encoded['Actual_Fare_PHP']
    
    print(f"\n✅ Preprocessing complete")
    print(f"   Features shape: {X.shape}")
    print(f"   Target shape: {y.shape}")
    
    return X, y, label_encoders


def train_model(X_train, y_train):
    """
    Train Random Forest model with optimized hyperparameters
    
    Args:
        X_train: Training features
        y_train: Training target
        
    Returns:
        RandomForestRegressor: Trained model
    """
    print("\n" + "="*50)
    print("Training Random Forest Model")
    print("="*50)
    
    # Initialize model with optimized hyperparameters
    model = RandomForestRegressor(
        n_estimators=100,           # Number of trees
        max_depth=20,                # Maximum depth of trees
        min_samples_split=5,         # Minimum samples to split node
        min_samples_leaf=2,          # Minimum samples at leaf
        max_features='sqrt',         # Number of features for best split
        random_state=42,             # Reproducibility
        n_jobs=-1,                   # Use all CPU cores
        verbose=1                    # Show progress
    )
    
    # Train model
    model.fit(X_train, y_train)
    
    print("\n✅ Model training complete")
    
    return model


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """
    Evaluate model performance on training and test sets
    
    Args:
        model: Trained model
        X_train, X_test: Feature sets
        y_train, y_test: Target sets
    """
    print("\n" + "="*50)
    print("Model Evaluation")
    print("="*50)
    
    # Training set predictions
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    
    # Test set predictions
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    print("\n📊 Training Set Performance:")
    print(f"   R² Score: {train_r2:.4f}")
    print(f"   Mean Absolute Error: ₱{train_mae:.2f}")
    print(f"   Root Mean Squared Error: ₱{train_rmse:.2f}")
    
    print("\n📊 Test Set Performance:")
    print(f"   R² Score: {test_r2:.4f}")
    print(f"   Mean Absolute Error: ₱{test_mae:.2f}")
    print(f"   Root Mean Squared Error: ₱{test_rmse:.2f}")
    
    # Cross-validation
    print("\n🔄 Cross-Validation (5-fold):")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                 scoring='r2', n_jobs=-1)
    print(f"   CV R² Scores: {cv_scores}")
    print(f"   Mean CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Check for overfitting
    if train_r2 - test_r2 > 0.1:
        print("\n⚠️  Warning: Possible overfitting detected")
        print(f"   Training R² ({train_r2:.4f}) significantly higher than Test R² ({test_r2:.4f})")
    else:
        print("\n✅ Good model generalization")


def analyze_feature_importance(model, feature_names):
    """
    Analyze and display feature importance
    
    Args:
        model: Trained model
        feature_names (list): Names of features
    """
    print("\n" + "="*50)
    print("Feature Importance Analysis")
    print("="*50)
    
    # Get feature importance
    importances = model.feature_importances_
    
    # Create DataFrame for better visualization
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances,
        'Percentage': importances * 100
    }).sort_values('Importance', ascending=False)
    
    print("\n📈 Feature Importance Ranking:")
    for idx, row in feature_importance_df.iterrows():
        bar_length = int(row['Percentage'] * 0.5)  # Scale for display
        bar = '█' * bar_length
        print(f"   {row['Feature']:20} {bar} {row['Percentage']:.2f}%")
    
    return feature_importance_df


def save_model(model, label_encoders, output_dir='backend'):
    """
    Save trained model and encoders to disk
    
    Args:
        model: Trained model
        label_encoders (dict): Label encoders for categorical variables
        output_dir (str): Output directory
    """
    print("\n" + "="*50)
    print("Saving Model")
    print("="*50)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, 'model.pkl')
    joblib.dump(model, model_path)
    print(f"✅ Model saved to: {model_path}")
    print(f"   File size: {os.path.getsize(model_path) / 1024:.2f} KB")
    
    # Save encoders (for reference)
    encoders_path = os.path.join(output_dir, 'label_encoders.pkl')
    joblib.dump(label_encoders, encoders_path)
    print(f"✅ Encoders saved to: {encoders_path}")


def test_predictions(model, X_test, y_test, n_samples=5):
    """
    Test model with sample predictions
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        n_samples (int): Number of samples to test
    """
    print("\n" + "="*50)
    print("Sample Predictions")
    print("="*50)
    
    # Select random samples
    indices = np.random.choice(len(X_test), n_samples, replace=False)
    
    print("\n🎯 Comparing Predictions vs Actual:")
    for i, idx in enumerate(indices, 1):
        actual = y_test.iloc[idx]
        predicted = model.predict(X_test.iloc[idx:idx+1])[0]
        error = abs(actual - predicted)
        error_pct = (error / actual) * 100
        
        print(f"\n   Sample {i}:")
        print(f"      Actual:    ₱{actual:.2f}")
        print(f"      Predicted: ₱{predicted:.2f}")
        print(f"      Error:     ₱{error:.2f} ({error_pct:.1f}%)")


def main():
    """
    Main training pipeline
    """
    print("="*50)
    print("Tricycle Fare Prediction Model Training")
    print("="*50)
    
    # Configuration
    DATA_FILE = 'tricycle_fare_data.csv'  # Change this to your dataset path
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    try:
        # Step 1: Load data
        df = load_data(DATA_FILE)
        
        # Step 2: Preprocess data
        X, y, label_encoders = preprocess_data(df)
        
        # Step 3: Split data
        print(f"\n📊 Splitting data (test size: {TEST_SIZE*100}%)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        print(f"   Training set: {X_train.shape[0]} samples")
        print(f"   Test set: {X_test.shape[0]} samples")
        
        # Step 4: Train model
        model = train_model(X_train, y_train)
        
        # Step 5: Evaluate model
        evaluate_model(model, X_train, X_test, y_train, y_test)
        
        # Step 6: Feature importance
        feature_names = ['Distance (km)', 'Fuel Price', 'Time of Day', 'Weather', 'Vehicle Type']
        analyze_feature_importance(model, feature_names)
        
        # Step 7: Test predictions
        test_predictions(model, X_test, y_test, n_samples=5)
        
        # Step 8: Save model
        save_model(model, label_encoders)
        
        print("\n" + "="*50)
        print("✅ Training Pipeline Complete!")
        print("="*50)
        print("\nNext steps:")
        print("1. Review the model performance metrics above")
        print("2. Check backend/model.pkl exists")
        print("3. Run the Flask backend: cd backend && python app.py")
        print("4. Test the API with sample requests")
        print("5. Deploy your application")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure your dataset CSV file exists.")
        print("Expected format:")
        print("  Distance_km,Fuel_Price,Time_of_Day,Weather,Vehicle_Type,Actual_Fare_PHP")
        print("  5.2,60-69,Rush Hour Morning,Sunny,Tricycle,45.00")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
