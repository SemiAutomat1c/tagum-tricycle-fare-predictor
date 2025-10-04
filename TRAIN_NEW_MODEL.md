# Training and Using the New Tagum Fare Model

## 📊 Model Performance

Based on your training results:
- **R² Score**: 0.998 (99.8% accuracy!)
- **Mean Absolute Error (MAE)**: ₱0.45
- **Mean Squared Error (MSE)**: 0.94

This is an **excellent** model performance! 🎉

## 🚀 Quick Start Guide

### Step 1: Prepare Your Dataset

Make sure `taGUM_FARE.csv` is in the project root directory.

### Step 2: Train the Model

Run the training script:

```bash
py train_tagum_model.py
```

This will:
- ✅ Load and clean the dataset (1002 samples)
- ✅ Encode categorical features properly
- ✅ Split data into training (80%) and testing (20%)
- ✅ Apply feature scaling
- ✅ Train the Random Forest model
- ✅ Evaluate model performance
- ✅ Save all pipeline components to `backend/` folder

**Files Generated:**
- `backend/model.pkl` - Trained Random Forest model
- `backend/preprocessor.pkl` - Data preprocessor (for encoding)
- `backend/scaler.pkl` - Feature scaler
- `backend/model_metadata.pkl` - Model performance metrics

### Step 3: Replace the Backend API

Replace the old `backend/app.py` with the new one:

```bash
# Windows
copy backend\app_new.py backend\app.py

# Linux/Mac
cp backend/app_new.py backend/app.py
```

Or manually rename:
1. Rename `backend/app.py` to `backend/app_old.py` (backup)
2. Rename `backend/app_new.py` to `backend/app.py`

### Step 4: Test the Backend

```bash
cd backend
py app.py
```

You should see:
```
✅ Model loaded successfully
✅ Preprocessor loaded successfully
✅ Scaler loaded successfully
✅ Metadata loaded successfully
   Model R² Score: 0.9980
   Model MAE: ₱0.45
```

The API will run on `http://localhost:5000`

### Step 5: Test a Prediction

Open a new terminal and test:

```bash
curl -X POST http://localhost:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Distance_km\": 5.5, \"Fuel_Price\": \"₱60-69\", \"Time_of_Day\": \"Rush Hour Morning\", \"Weather\": \"Sunny\", \"Vehicle_Type\": \"Tricycle\"}"
```

Expected response:
```json
{
  "predicted_fare": 32.45,
  "input": { ... }
}
```

### Step 6: Test the Frontend

1. Open `index.html` in your browser
2. Set origin and destination
3. Fill in the fare parameters
4. Click "Predict Fare"
5. See the accurate prediction! ✨

## 📝 Important Changes

### 1. Fuel Price Format
The new model uses **₱** symbol in fuel prices:
- ❌ Old: `"60-69"`
- ✅ New: `"₱60-69"`

The frontend has been updated to send the correct format.

### 2. Model Pipeline
The new model uses a complete pipeline:
1. **Preprocessor**: Handles ordinal encoding (Fuel_Price) and one-hot encoding (other categories)
2. **Scaler**: StandardScaler for feature normalization
3. **Model**: Random Forest Regressor

### 3. API Updates
New `/valid-values` endpoint to check accepted input values:
```bash
curl http://localhost:5000/valid-values
```

## 🔍 Model Details

### Dataset Information
- **Total Samples**: 1,002
- **Training Samples**: 801 (80%)
- **Testing Samples**: 201 (20%)

### Features Used
1. **Distance_km** (numerical) - Distance in kilometers
2. **Fuel_Price** (ordinal) - Fuel price range with ₱ symbol
3. **Time_of_Day** (categorical) - Rush Hour Morning, Off-Peak, Rush Hour Evening
4. **Weather** (categorical) - Sunny, Rainy
5. **Vehicle_Type** (categorical) - Single Motor, Tricycle

### Model Configuration
```python
RandomForestRegressor(
    n_estimators=100,  # 100 decision trees
    random_state=42
)
```

## 🐛 Troubleshooting

### Error: "Model file not found"
**Solution**: Run `py train_tagum_model.py` first to generate the model files.

### Error: "Invalid Fuel_Price"
**Solution**: Make sure fuel prices include the ₱ symbol (e.g., `₱60-69`)

### Error: "Pipeline components not loaded"
**Solution**: 
1. Check that all 4 `.pkl` files exist in `backend/` folder
2. Restart the backend server
3. Check console logs for specific errors

### Frontend not working
**Solution**:
1. Make sure backend is running on port 5000
2. Check browser console for errors
3. Verify the fuel price dropdown values include ₱ symbol

## 📊 Model Performance Breakdown

```
Training Set:
  - Samples: 801
  - Expected very high accuracy (training data)

Test Set:
  - Samples: 201  
  - R² Score: 0.998 (99.8%)
  - MAE: ₱0.45 (very low error!)
  - MSE: 0.94

Feature Importance (typical):
  1. Distance_km - Highest importance
  2. Fuel_Price - Second
  3. Time_of_Day - Third
  4. Weather - Fourth
  5. Vehicle_Type - Fifth
```

## 🚀 Deployment

### Backend Deployment (Render/Railway)

1. Make sure `backend/app.py` uses the new version
2. Commit all `.pkl` files to Git
3. Deploy to Render/Railway
4. The model files will be included in the deployment

### Frontend Deployment (Vercel)

The frontend already has the updated fuel price format, so no changes needed!

## ✅ Checklist

Before deploying:
- [ ] Trained model using `py train_tagum_model.py`
- [ ] All 4 `.pkl` files exist in `backend/` folder
- [ ] Replaced `backend/app.py` with the new version
- [ ] Tested backend locally on port 5000
- [ ] Tested frontend prediction with new model
- [ ] Verified R² score is 0.998
- [ ] Frontend fuel prices include ₱ symbol
- [ ] Committed all changes to Git

## 🎉 Success!

Your new model with **99.8% accuracy** is now ready to use! The average prediction error is only **₱0.45**, which means your fare predictions will be extremely accurate! 

---

**Questions?** Check the console logs when running the backend for detailed information about model loading and predictions.

