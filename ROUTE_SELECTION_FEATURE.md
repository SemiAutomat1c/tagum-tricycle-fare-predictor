# Route Selection Feature

## Overview
The Tricycle Fare Optimizer now allows users to choose between multiple route options when calculating fares between two locations.

## How It Works

### 1. **Multiple Route Calculation**
When you set an origin and destination and click "Calculate Route", the application now:
- Requests up to 3 alternative routes from the OSRM routing service
- Displays all available routes on the map
- Shows route options in a selection panel

### 2. **Visual Differentiation**
- **Selected Route**: Displayed in blue (`#2563eb`) with thicker lines (5px weight, 80% opacity)
- **Alternative Routes**: Displayed in gray (`#94a3b8`) with thinner lines (3px weight, 40% opacity)

### 3. **Route Selection Methods**

#### Method A: Click on Route Cards
- Route options appear in a panel above the fare prediction form
- Each card shows:
  - Route number (Route 1, Route 2, etc.)
  - Distance in kilometers
  - Estimated duration in minutes
  - "Selected" badge for the current route
- Click on any card to select that route

#### Method B: Click on Map
- Click directly on any route line on the map to select it
- The selected route will highlight and the UI will update

### 4. **Automatic Updates**
When you select a different route:
- The map updates to highlight the selected route
- The distance field updates with the new route's distance
- The route cards update to show which is selected
- Any fare prediction will use the selected route's distance

## Technical Details

### API Request
```javascript
// OSRM endpoint with alternatives parameter
https://router.project-osrm.org/route/v1/driving/{origin};{destination}?overview=full&geometries=geojson&alternatives=3
```

### Key Functions
- `calculateRoute()`: Fetches multiple routes from OSRM
- `displayAllRoutes()`: Renders all routes on the map
- `selectRoute(index)`: Switches to a different route
- `updateRouteSelector()`: Updates the UI cards

### State Management
```javascript
let availableRoutes = [];      // Array of all route objects from OSRM
let routeLines = [];            // Array of Leaflet polyline objects
let selectedRouteIndex = 0;     // Currently selected route index
let currentRoute = null;        // Currently selected route object
```

## UI Components

### HTML
- `#routeOptionsContainer`: Container for route selection cards
- Dynamically generated route option cards with distance and duration

### CSS Classes
- `.route-options-container`: Main container styling
- `.route-option`: Individual route card
- `.route-option.selected`: Selected route highlighting
- `.route-badge`: "Selected" badge styling
- `.route-detail`: Distance and duration display

## Benefits

1. **Flexibility**: Choose the route that best suits your needs (shortest, fastest, or avoiding certain areas)
2. **Transparency**: See all available options at once
3. **Better Estimates**: Select the route you actually plan to take for more accurate fare predictions
4. **Visual Clarity**: Easily compare routes on the map

## Fallback Behavior

- If only one route is available, the selection panel is hidden
- The system automatically selects the first (optimal) route by default
- Works seamlessly with the existing fare prediction system

## Browser Compatibility

Works on all modern browsers that support:
- ES6+ JavaScript (arrow functions, const/let)
- Fetch API
- Leaflet.js for mapping

