# Getting Started with Tricycle Fare Optimizer

**Welcome!** This guide will help you get the application running in minutes.

## 📋 What You'll Need

- ✅ Python 3.8 or higher
- ✅ A modern web browser (Chrome, Firefox, Safari, Edge)
- ✅ Internet connection (for map tiles and routing)
- ✅ 10 minutes of your time

## 🎯 What This Application Does

This web app helps predict tricycle fares in Tagum City by:
1. Letting users select origin and destination on an interactive map
2. Calculating the actual route using real road networks
3. Using machine learning to predict the fare based on:
   - Distance
   - Fuel prices
   - Time of day
   - Weather conditions
   - Vehicle type

## 🚀 Three Simple Steps

### Step 1: Setup Environment

**Windows Users:**
```bash
# Open Command Prompt or PowerShell in the project directory
setup.bat
```

**Mac/Linux Users:**
```bash
# Open Terminal in the project directory
chmod +x setup.sh
./setup.sh
```

This script will:
- ✅ Check if Python is installed
- ✅ Create a virtual environment
- ✅ Install all required packages
- ✅ Check for the model file

### Step 2: Create Model (If You Don't Have One)

If you see "WARNING: model.pkl not found", run these commands:

**Windows:**
```bash
# Generate sample data
py sample_data_generator.py

# Train the model
py train_model.py
```

**Mac/Linux:**
```bash
# Generate sample data
python3 sample_data_generator.py

# Train the model
python3 train_model.py
```

The training script will:
- ✅ Load the dataset
- ✅ Process the data
- ✅ Train a Random Forest model
- ✅ Save `model.pkl` in the `backend/` folder

### Step 3: Run the Application

**Start the Backend:**

**Windows:**
```bash
cd backend
venv\Scripts\activate
py app.py
```

**Mac/Linux:**
```bash
cd backend
source venv/bin/activate
python3 app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
Model loaded successfully
```

**Open the Frontend:**

Option 1 - Direct File:
- Simply double-click `index.html` in the project folder

Option 2 - HTTP Server (Recommended):
```bash
# In a new terminal, from the project root
python -m http.server 8000
```
Then open your browser to: `http://localhost:8000`

## 🎮 Using the Application

### First Time Use

1. **Allow Location Access** (Optional)
   - When prompted, click "Allow" to use your current location
   - Or skip and manually set your origin

2. **Set Origin Point**
   - Your current location appears as a blue marker (if GPS enabled)
   - Click "Change Origin Point" to manually select
   - Drag the blue marker to adjust position

3. **Set Destination**
   - Click anywhere on the map to place a red destination marker
   - The route will automatically calculate

4. **Enter Parameters**
   - Fill in all the dropdown fields:
     - Fuel Price Range (current fuel cost)
     - Time of Day (when you're traveling)
     - Weather Condition (current/expected)
     - Vehicle Type (motor or tricycle)

5. **Get Prediction**
   - Click "Predict Fare" button
   - Wait for the result (appears in green)

6. **Try Another Route**
   - Click "Reset Route" to start over
   - Origin stays, destination clears

## 🧪 Testing

### Test the Backend API

```bash
# In a new terminal
py test_api.py           # Windows
python3 test_api.py      # Mac/Linux
```

This will run automated tests and show if everything works.

### Manual Test

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

## ❓ Common Issues & Solutions

### "Python not found"
**Solution:** Install Python from [python.org](https://python.org)
- ✅ Check "Add Python to PATH" during installation
- ✅ Restart your terminal after installation

### "Cannot connect to prediction server"
**Solution:** Make sure backend is running
```bash
# Check if backend is running
curl http://localhost:5000/health
```
If not running, start it:
```bash
cd backend
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
python app.py
```

### "Model not found"
**Solution:** Train the model
```bash
python sample_data_generator.py
python train_model.py
```
Verify `backend/model.pkl` exists.

### "Route not calculating"
**Possible Causes:**
- No internet connection (OSRM API requires internet)
- Points too far apart
- No road route between points

**Solution:**
- Check internet connection
- Try different locations closer together
- Check browser console for errors (F12)

### "Location not detected"
**Solution:** 
- Check browser location permissions
- Use "Change Origin Point" to manually set
- Chrome: Settings → Privacy → Site Settings → Location
- Firefox: Preferences → Privacy & Security → Permissions

### Port 5000 already in use
**Solution:** Change the port
In `backend/app.py`, change the last line:
```python
app.run(host='0.0.0.0', port=5001)  # Use 5001 instead
```
Then update `app.js`:
```javascript
backendAPI: 'http://localhost:5001/predict'
```

## 📚 Next Steps

### For Development
1. **Customize the UI**: Edit `style.css` for your branding
2. **Adjust Map**: Change center coordinates in `app.js`
3. **Modify Model**: Retrain with your own data

### For Production
1. **Deploy Frontend**: Push to GitHub and deploy on Vercel
2. **Deploy Backend**: Use Render.com or Railway.app
3. **Update API URL**: Change `backendAPI` in `app.js`
4. **Configure CORS**: Update allowed origins in `backend/app.py`

See `README.md` for detailed deployment instructions.

### Using Your Own Data

Replace the sample data with real fare data:

1. Create CSV file with these exact columns:
   ```
   Distance_km,Fuel_Price,Time_of_Day,Weather,Vehicle_Type,Actual_Fare_PHP
   ```

2. Ensure categorical values match exactly:
   - Fuel_Price: "20-29", "30-39", etc.
   - Time_of_Day: "Rush Hour Morning", "Off-Peak", "Rush Hour Evening"
   - Weather: "Sunny", "Rainy"
   - Vehicle_Type: "Single Motor", "Tricycle"

3. Save as `tricycle_fare_data.csv`

4. Train model:
   ```bash
   python train_model.py
   ```

## 📖 Documentation

- **README.md** - Complete project documentation
- **QUICKSTART.md** - Quick reference guide
- **PROJECT_SUMMARY.md** - Technical summary and checklist
- **backend/README.md** - API documentation
- **STRUCTURE.txt** - File organization

## 💡 Tips

1. **Development Mode**: Keep backend terminal open to see logs
2. **Browser Console**: Press F12 to see detailed error messages
3. **API Testing**: Use `test_api.py` to verify backend works
4. **Sample Predictions**: Test with known routes first
5. **Model Retraining**: Update dataset and retrain for better accuracy

## 🎓 Understanding the Code

### Frontend (`app.js`)
- `initializeMap()` - Sets up Leaflet map
- `detectUserLocation()` - Gets GPS coordinates
- `calculateRoute()` - Calls OSRM API
- `handlePrediction()` - Sends data to backend

### Backend (`backend/app.py`)
- `load_model()` - Loads the trained model
- `validate_input_data()` - Checks request data
- `/predict` - Main prediction endpoint

### Model Training (`train_model.py`)
- `load_data()` - Reads CSV dataset
- `preprocess_data()` - Encodes categories
- `train_model()` - Trains Random Forest
- `save_model()` - Exports to backend/

## 🆘 Need Help?

1. **Check logs**: Backend terminal shows detailed errors
2. **Browser console**: F12 shows frontend errors
3. **Test API**: Run `test_api.py` to diagnose
4. **Review docs**: See README.md troubleshooting section
5. **Sample data**: Use provided generator if no real data

## ✨ Features at a Glance

| Feature | Status |
|---------|--------|
| Interactive Map | ✅ |
| GPS Location | ✅ |
| Route Calculation | ✅ |
| Fare Prediction | ✅ |
| Mobile Responsive | ✅ |
| Error Handling | ✅ |
| API Testing | ✅ |
| Documentation | ✅ |

## 🎉 You're Ready!

Follow the three steps above and you'll have a working fare prediction system.

**Questions?** Check the README.md or documentation files.

**Ready to deploy?** See the deployment section in README.md.

---

**Built with ❤️ for Tagum City**

Happy predicting! 🛺
