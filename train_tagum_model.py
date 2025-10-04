# =============================================================================
# Tagum Tricycle Fare Prediction Model Training Script
# =============================================================================

# Import necessary libraries for data handling
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

print("="*60)
print("   Tagum Tricycle Fare Prediction Model Training")
print("="*60)

# =============================================================================
# Step 1: Load the Dataset
# =============================================================================
print("\n📂 Loading dataset...")
df = pd.read_csv('taGUM_FARE.csv')

print("✅ Dataset loaded successfully!")
print("-----------------------------------")
print("First 5 rows of the dataset:")
print(df.head())

print("\n-----------------------------------")
print("Dataset information:")
df.info()

print("\n----------- Descriptive Statistics -----------")
print(df.describe())
print("\n" + "="*60 + "\n")

# =============================================================================
# Step 2: Data Cleaning & Encoding
# =============================================================================
print("🧹 Cleaning and encoding data...")

# --- 1. Separate features (X) from the target variable (y) ---
X = df.drop('Actual_Fare_PHP', axis=1)
y = df['Actual_Fare_PHP']

# --- 2. Data Cleaning Step ---
# Replace '?' character with '₱' symbol in Fuel_Price column
print("   Cleaning the 'Fuel_Price' column...")
X['Fuel_Price'] = X['Fuel_Price'].str.replace('?', '₱', regex=False)
print(f"   Cleaned sample value: {X['Fuel_Price'].iloc[0]}")

# --- 3. Define the explicit order for the 'Fuel_Price' feature ---
fuel_price_order = [
    '₱20-29', '₱30-39', '₱40-49', '₱50-59',
    '₱60-69', '₱70-79', '₱80-89', '₱90-99', '₱100 & up'
]

# --- 4. Identify which columns need which type of encoding ---
ordinal_features = ['Fuel_Price']
onehot_features = ['Time_of_Day', 'Weather', 'Vehicle_Type']

# --- 5. Create a ColumnTransformer to apply the encoding ---
preprocessor = ColumnTransformer(
    transformers=[
        ('ordinal', OrdinalEncoder(categories=[fuel_price_order]), ordinal_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore'), onehot_features)
    ],
    remainder='passthrough'
)

# --- 6. Apply the preprocessor to the features (X) ---
X_processed = preprocessor.fit_transform(X)

print("✅ Categorical data has been successfully encoded.")
print("--------------------------------------------------")
print(f"Shape of the processed feature matrix (X): {X_processed.shape}")
print(f"Sample of the first row after processing:")
print(X_processed[0])

# =============================================================================
# Step 3: Splitting the Dataset
# =============================================================================
print("\n📊 Splitting data into training and testing sets...")

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42
)

print("✅ Data has been split successfully.")
print("-----------------------------------------------------")
print(f"Training features (X_train) shape: {X_train.shape}")
print(f"Testing features (X_test) shape:  {X_test.shape}")
print(f"Training target (y_train) shape: {y_train.shape}")
print(f"Testing target (y_test) shape:  {y_test.shape}")

# =============================================================================
# Step 4: Feature Scaling
# =============================================================================
print("\n⚖️  Applying feature scaling...")

scaler = StandardScaler(with_mean=False)
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Feature scaling (Standardization) has been applied.")
print("------------------------------------------------------")

# =============================================================================
# Step 5: Training the Random Forest Model
# =============================================================================
print("\n🌲 Training the Random Forest model...")
print("   (This may take a minute...)")

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, verbose=1)
rf_model.fit(X_train_scaled, y_train)

print("\n✅ Model training is complete!")

# =============================================================================
# Step 6: Evaluating the Model
# =============================================================================
print("\n📈 Evaluating model performance...")

# Make predictions on the scaled test data
predictions = rf_model.predict(X_test_scaled)

# Calculate the performance metrics
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Print the results
print("\n" + "="*60)
print("   📊 MODEL PERFORMANCE ON TEST SET")
print("="*60)

print(f"\n✨ Mean Absolute Error (MAE): ₱{mae:.2f}")
print(f"   → On average, the model's prediction is off by {mae:.2f} pesos")

print(f"\n✨ Mean Squared Error (MSE): {mse:.2f}")
print(f"   → This metric penalizes larger errors more heavily")

print(f"\n✨ R-squared (R²): {r2:.4f} ({r2:.1%})")
print(f"   → The model explains {r2:.1%} of the variation in fares")

if r2 > 0.95:
    print("\n🎉 EXCELLENT MODEL PERFORMANCE!")
elif r2 > 0.85:
    print("\n👍 GOOD MODEL PERFORMANCE!")
else:
    print("\n⚠️  Model performance could be improved")

print("\n" + "="*60)

# =============================================================================
# Step 7: Feature Importance Analysis
# =============================================================================
print("\n📊 Feature Importance Analysis...")

# Get feature names after transformation
feature_names = []
# Ordinal feature
feature_names.append('Fuel_Price')
# OneHot encoded features
onehot_encoder = preprocessor.named_transformers_['onehot']
for i, feature in enumerate(onehot_features):
    feature_names.extend([f"{feature}_{cat}" for cat in onehot_encoder.categories_[i]])
# Passthrough feature (Distance_km)
feature_names.append('Distance_km')

# Get feature importances
importances = rf_model.feature_importances_

# Create DataFrame for better visualization
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values('Importance', ascending=False)

print("\n📈 Top 10 Most Important Features:")
print("="*60)
for idx, row in feature_importance_df.head(10).iterrows():
    bar_length = int(row['Importance'] * 100)
    bar = '█' * bar_length
    print(f"{row['Feature']:30} {bar} {row['Importance']:.4f}")

# =============================================================================
# Step 8: Sample Predictions
# =============================================================================
print("\n" + "="*60)
print("   🎯 SAMPLE PREDICTIONS (5 random test cases)")
print("="*60)

# Select 5 random samples
indices = np.random.choice(len(X_test), 5, replace=False)

for i, idx in enumerate(indices, 1):
    actual = y_test.iloc[idx]
    predicted = predictions[idx]
    error = abs(actual - predicted)
    error_pct = (error / actual) * 100
    
    print(f"\nSample {i}:")
    print(f"   Actual Fare:    ₱{actual:.2f}")
    print(f"   Predicted Fare: ₱{predicted:.2f}")
    print(f"   Error:          ₱{error:.2f} ({error_pct:.1f}%)")

# =============================================================================
# Step 9: Save the Model and Pipeline Components
# =============================================================================
print("\n" + "="*60)
print("   💾 SAVING MODEL AND PIPELINE COMPONENTS")
print("="*60)

# Create backend directory if it doesn't exist
backend_dir = 'backend'
os.makedirs(backend_dir, exist_ok=True)

# Save the trained Random Forest model
model_path = os.path.join(backend_dir, 'model.pkl')
joblib.dump(rf_model, model_path)
print(f"✅ Random Forest model saved to: {model_path}")
print(f"   File size: {os.path.getsize(model_path) / 1024:.2f} KB")

# Save the preprocessor (for encoding)
preprocessor_path = os.path.join(backend_dir, 'preprocessor.pkl')
joblib.dump(preprocessor, preprocessor_path)
print(f"✅ Preprocessor saved to: {preprocessor_path}")
print(f"   File size: {os.path.getsize(preprocessor_path) / 1024:.2f} KB")

# Save the scaler
scaler_path = os.path.join(backend_dir, 'scaler.pkl')
joblib.dump(scaler, scaler_path)
print(f"✅ Scaler saved to: {scaler_path}")
print(f"   File size: {os.path.getsize(scaler_path) / 1024:.2f} KB")

# Save model metadata for reference
metadata = {
    'mae': mae,
    'mse': mse,
    'r2': r2,
    'n_samples_train': len(X_train),
    'n_samples_test': len(X_test),
    'fuel_price_order': fuel_price_order,
    'ordinal_features': ordinal_features,
    'onehot_features': onehot_features
}

metadata_path = os.path.join(backend_dir, 'model_metadata.pkl')
joblib.dump(metadata, metadata_path)
print(f"✅ Model metadata saved to: {metadata_path}")

# =============================================================================
# Step 10: Summary
# =============================================================================
print("\n" + "="*60)
print("   🎉 TRAINING PIPELINE COMPLETE!")
print("="*60)

print("\n📋 Summary:")
print(f"   • Dataset size: {len(df)} samples")
print(f"   • Training samples: {len(X_train)}")
print(f"   • Test samples: {len(X_test)}")
print(f"   • Model R² Score: {r2:.4f}")
print(f"   • Mean Absolute Error: ₱{mae:.2f}")

print("\n📁 Files saved in 'backend/' directory:")
print("   • model.pkl - Trained Random Forest model")
print("   • preprocessor.pkl - Data preprocessor")
print("   • scaler.pkl - Feature scaler")
print("   • model_metadata.pkl - Model performance metadata")

print("\n🚀 Next Steps:")
print("   1. Update backend/app.py to use the new model")
print("   2. Test the backend API: cd backend && py app.py")
print("   3. Test predictions with the frontend")
print("   4. Deploy the updated application")

print("\n" + "="*60)
print("✅ All done! Your model is ready to use.")
print("="*60 + "\n")

