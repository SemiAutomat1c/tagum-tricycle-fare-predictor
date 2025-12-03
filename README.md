# 🛺 Tagum Tricycle Fare Predictor

> An intelligent web application that predicts tricycle fares in Tagum City using machine learning, interactive mapping, and real-time route calculation.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

## 🌟 Overview

The Tagum Tricycle Fare Predictor is a modern web application designed to help residents and visitors of Tagum City estimate tricycle fares accurately. By combining machine learning with real-time route calculation, the app provides fair and transparent fare estimates based on actual road distances, weather conditions, time of day, and other factors.

## ✨ Key Features

### 🗺️ **Smart Route Selection**
- **Multiple Route Options**: Choose from up to 3 alternative routes between your origin and destination
- **Visual Route Comparison**: See all routes on the map simultaneously with clear visual differentiation
- **Real-time Route Details**: Compare distance and estimated duration for each route
- **Interactive Selection**: Click on route cards or directly on map routes to switch between options

### 📍 **Intelligent Location Services**
- **GPS Auto-Detection**: Automatically finds your current location with permission
- **Manual Origin Selection**: Click anywhere on the map to set your starting point
- **Flexible Destination**: Easy destination marking with a simple click
- **Draggable Markers**: Adjust your origin by dragging the blue marker

### 🛣️ **Accurate Route Calculation**
- **Real Road Distances**: Uses OSRM (Open Source Routing Machine) for precise calculations
- **No Straight Lines**: Follows actual road networks for realistic distances
- **Live Route Visualization**: See your route drawn on the map in real-time
- **Auto-Fit View**: Map automatically adjusts to show your entire route

### 🤖 **Machine Learning Powered**
- **Random Forest Model**: Trained on Tagum City tricycle fare data
- **Multi-Factor Analysis**: Considers distance, fuel prices, time of day, weather, and vehicle type
- **Instant Predictions**: Get fare estimates in milliseconds
- **Transparent Results**: See the factors used in your fare calculation

### 💰 **Dynamic Fare Factors**
- **Distance-Based Pricing**: Calculated from actual road routes
- **Fuel Price Adjustment**: Multiple price ranges from ₱20 to ₱100+
- **Peak Hour Pricing**: Accounts for rush hour morning, evening, and off-peak times
- **Weather Conditions**: Adjusts for sunny or rainy weather
- **Vehicle Type**: Supports both single motor and tricycle options

### 📱 **Modern User Experience**
- **Fully Responsive**: Seamless experience on mobile, tablet, and desktop
- **Clean Interface**: Modern, intuitive design with Tagum City branding
- **Real-time Feedback**: Loading states, success animations, and clear error messages
- **2-Column Form Layout**: Compact, efficient parameter selection
- **One-Page Design**: No scrolling needed for fare prediction

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3**: Modern, semantic markup with responsive design
- **Vanilla JavaScript (ES6+)**: No framework overhead, fast performance
- **Leaflet.js 1.9.4**: Industry-standard interactive mapping
- **OpenStreetMap**: Free, open-source map data
- **OSRM API**: Professional-grade routing engine

### Backend
- **Firebase Cloud Functions (2nd Gen)**: Serverless Python backend
- **Flask 3.0.0**: Lightweight framework adapted for serverless
- **scikit-learn 1.5.2**: Robust machine learning library
- **Random Forest Regressor**: Optimized for fare prediction
- **pandas 2.2.3**: Efficient data handling

## 📖 How to Use

### 1. **Set Your Starting Point**
   - Allow location access when prompted, OR
   - Click "Change Origin Point" and click on the map

### 2. **Choose Your Destination**
   - Click anywhere on the map to set your destination, OR
   - Use the search bar to find popular destinations

### 3. **Calculate Routes**
   - Routes are automatically calculated when you set both points
   - If multiple routes are available, you'll see a "Available Routes" panel
   - Click on any route card to select it, or click directly on a route line

### 4. **Review Route Options** (if multiple routes found)
   - Compare distances and estimated travel times
   - Selected route is highlighted in blue
   - Alternative routes shown in gray
   - Distance field updates automatically when you switch routes

### 5. **Enter Fare Parameters**
   - **Fuel Price**: Current fuel price range in Tagum City
   - **Time of Day**: Rush hour morning, off-peak, or rush hour evening
   - **Weather**: Current weather conditions
   - **Vehicle Type**: Single motor or tricycle

### 6. **Get Your Fare Estimate**
   - Click "Predict Fare"
   - See your estimated fare in Philippine Pesos (₱)
   - Review all factors used in the calculation

## 🎯 Use Cases

### For Passengers
- **Budget Planning**: Know the expected fare before your trip
- **Fair Pricing**: Verify you're being charged appropriately
- **Route Comparison**: Choose the best route for your needs
- **Trip Planning**: Estimate costs for daily commutes

### For Drivers
- **Fare Reference**: Professional fare calculation tool
- **Customer Transparency**: Show passengers how fares are calculated
- **Route Optimization**: Compare route options with passengers
- **Fair Pricing**: Ensure competitive, fair pricing

### For Tourists & Visitors
- **No Surprises**: Know fares before traveling
- **Explore Confidently**: Navigate Tagum City with confidence
- **Budget Travel**: Plan expenses accurately
- **Route Discovery**: Find the best routes to destinations

## 🌐 Live Demo

**Live App**: [Deployed on Firebase](https://tagum-fare-predictor-v2.web.app)

## 📊 Fare Prediction Accuracy

Our machine learning model has been trained on real Tagum City tricycle fare data with the following performance metrics:

- **R² Score**: Measures how well the model fits the data
- **Mean Absolute Error (MAE)**: Average prediction error
- **Root Mean Squared Error (RMSE)**: Penalizes larger errors

The model considers multiple factors to provide accurate, fair fare estimates that reflect real-world pricing.

## 🔒 Privacy & Data

- **No Personal Data Stored**: Location data is never saved or transmitted to third parties
- **GPS Permission**: Only used for convenience, not required
- **Anonymous Predictions**: No user tracking or profiling
- **Open Source**: Fully transparent codebase
- **Secure API**: CORS-enabled, validated requests only

## 📱 Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Performance

- ⚡ **Fast Loading**: Optimized assets, minimal dependencies
- 🗺️ **Lazy Map Loading**: Map tiles load as needed
- 🔄 **Instant Route Switching**: No delays when selecting routes
- 💨 **Quick API Response**: Predictions in < 500ms

## 🎨 Design Principles

- **Mobile-First**: Designed for smartphone use
- **Accessible**: WCAG 2.1 compliant
- **Intuitive**: No learning curve
- **Modern**: Clean, professional interface
- **Local**: Tagum City branding and context

## 🗺️ Coverage Area

Optimized for **Tagum City, Davao del Norte, Philippines**

- Centered on coordinates: 7.4474°N, 125.8072°E
- Covers all major roads and barangays
- Includes popular destinations:
  - Gaisano Mall of Tagum
  - Tagum City Hall
  - New Tagum City Public Market
  - Energy Park
  - And many more!

## 🔧 Technical Features

### Route Selection System
- Requests up to 3 alternative routes from OSRM
- Visual differentiation (blue = selected, gray = alternatives)
- Click-to-select on route cards or map lines
- Automatic distance field updates
- Real-time route comparison panel

### Smart UI
- 2-column grid layout for parameters
- Compact spacing for one-page view
- Responsive route option cards
- Context-aware route panel (hidden when only 1 route)
- Loading states and success animations

### API Integration
- OSRM for routing: `https://router.project-osrm.org/route/v1/driving`
- Custom Flask backend for fare prediction
- Automatic environment detection (localhost vs production)
- Error handling with user-friendly messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap Contributors**: For free, open map data
- **OSRM Project**: For powerful routing capabilities
- **Leaflet.js Team**: For excellent mapping library
- **scikit-learn Community**: For machine learning tools
- **Tagum City**: For inspiring this project

## 🤝 Contributing

This is an open-source project. Contributions, issues, and feature requests are welcome!

## 📧 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the documentation in the `/docs` folder
- Review the code comments for implementation details

## 🎯 Project Status

**Active Development** - Continuously improving with new features and optimizations.

### Recent Updates
- ✅ Multi-route selection feature
- ✅ Compact 2-column parameter layout
- ✅ Improved visual route differentiation
- ✅ Enhanced mobile responsiveness
- ✅ Optimized for one-page view

---

**Built with ❤️ for Tagum City** 🛺

*Making tricycle fares transparent, fair, and predictable.*
