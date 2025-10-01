// ============================================
// Tricycle Fare Optimizer - Main Application
// ============================================

// Configuration
const CONFIG = {
    // Tagum City coordinates
    tagumCity: {
        lat: 7.4474,
        lng: 125.8072
    },
    defaultZoom: 14,
    // OSRM routing API endpoint
    osrmEndpoint: 'https://router.project-osrm.org/route/v1/driving',
    // Backend API endpoint - automatically detects local vs deployed
    backendAPI: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000/predict'
        : 'https://tagum-tricycle-fare-api.onrender.com/predict' // Update after deploying to Render
};

// Global state
let map;
let originMarker = null;
let destinationMarker = null;
let routeLine = null;
let currentRoute = null;
let isSettingOrigin = false;

// ============================================
// Map Initialization
// ============================================

/**
 * Initialize the Leaflet map with OpenStreetMap tiles
 */
function initializeMap() {
    // Create map centered on Tagum City
    map = L.map('map').setView([CONFIG.tagumCity.lat, CONFIG.tagumCity.lng], CONFIG.defaultZoom);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Add map click event listener for destination selection
    map.on('click', handleMapClick);
    
    console.log('Map initialized successfully');
}

/**
 * Handle map click events for setting origin or destination
 */
function handleMapClick(e) {
    const { lat, lng } = e.latlng;
    
    if (isSettingOrigin) {
        // Setting new origin
        setOrigin(lat, lng);
        isSettingOrigin = false;
        document.getElementById('changeOriginBtn').textContent = '📍 Change Origin Point';
    } else {
        // Setting destination
        setDestination(lat, lng);
    }
}

// ============================================
// Location Detection
// ============================================

/**
 * Request and detect user's current location
 */
function detectUserLocation() {
    if ('geolocation' in navigator) {
        console.log('Requesting geolocation permission...');
        
        navigator.geolocation.getCurrentPosition(
            // Success callback
            (position) => {
                const { latitude, longitude } = position.coords;
                console.log(`Location detected: ${latitude}, ${longitude}`);
                
                setOrigin(latitude, longitude);
                map.setView([latitude, longitude], CONFIG.defaultZoom);
                
                showNotification('Location detected successfully!', 'success');
            },
            // Error callback
            (error) => {
                console.error('Geolocation error:', error);
                
                let message = 'Location access denied. ';
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        message += 'Please enable location access or use "Change Origin" button.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        message += 'Location information unavailable.';
                        break;
                    case error.TIMEOUT:
                        message += 'Location request timed out.';
                        break;
                }
                
                alert(message);
                
                // Default to Tagum City center
                setOrigin(CONFIG.tagumCity.lat, CONFIG.tagumCity.lng);
            },
            // Options
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert('Geolocation is not supported by your browser. Defaulting to Tagum City center.');
        setOrigin(CONFIG.tagumCity.lat, CONFIG.tagumCity.lng);
    }
}

// ============================================
// Marker Management
// ============================================

/**
 * Set origin marker on the map
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 */
function setOrigin(lat, lng) {
    // Remove existing origin marker
    if (originMarker) {
        map.removeLayer(originMarker);
    }
    
    // Create custom blue icon for origin
    const blueIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="42" viewBox="0 0 32 42">
                <path fill="#2563eb" stroke="#ffffff" stroke-width="2" d="M16 0C9.373 0 4 5.373 4 12c0 8.25 12 30 12 30s12-21.75 12-30c0-6.627-5.373-12-12-12z"/>
                <circle cx="16" cy="12" r="5" fill="#ffffff"/>
            </svg>
        `),
        iconSize: [32, 42],
        iconAnchor: [16, 42],
        popupAnchor: [0, -42]
    });
    
    // Add origin marker (draggable)
    originMarker = L.marker([lat, lng], {
        icon: blueIcon,
        draggable: true,
        title: 'Origin (Draggable)'
    }).addTo(map);
    
    originMarker.bindPopup('<b>Origin</b><br>Drag to adjust position').openPopup();
    
    // Add drag event
    originMarker.on('dragend', function(e) {
        const { lat, lng } = e.target.getLatLng();
        updateOriginCoordinates(lat, lng);
        
        // Recalculate route if destination exists
        if (destinationMarker) {
            calculateRoute();
        }
    });
    
    updateOriginCoordinates(lat, lng);
    
    // Recalculate route if destination exists
    if (destinationMarker) {
        calculateRoute();
    }
}

/**
 * Set destination marker on the map
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 */
function setDestination(lat, lng) {
    // Remove existing destination marker
    if (destinationMarker) {
        map.removeLayer(destinationMarker);
    }
    
    // Create custom red icon for destination
    const redIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="42" viewBox="0 0 32 42">
                <path fill="#dc2626" stroke="#ffffff" stroke-width="2" d="M16 0C9.373 0 4 5.373 4 12c0 8.25 12 30 12 30s12-21.75 12-30c0-6.627-5.373-12-12-12z"/>
                <circle cx="16" cy="12" r="5" fill="#ffffff"/>
            </svg>
        `),
        iconSize: [32, 42],
        iconAnchor: [16, 42],
        popupAnchor: [0, -42]
    });
    
    // Add destination marker
    destinationMarker = L.marker([lat, lng], {
        icon: redIcon,
        title: 'Destination'
    }).addTo(map);
    
    destinationMarker.bindPopup('<b>Destination</b>').openPopup();
    
    updateDestinationCoordinates(lat, lng);
    
    // Calculate route
    calculateRoute();
}

/**
 * Update origin coordinates display
 */
function updateOriginCoordinates(lat, lng) {
    document.getElementById('originCoords').textContent = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
}

/**
 * Update destination coordinates display
 */
function updateDestinationCoordinates(lat, lng) {
    document.getElementById('destCoords').textContent = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
}

// ============================================
// Route Calculation (OSRM)
// ============================================

/**
 * Calculate route using OSRM API
 */
async function calculateRoute() {
    if (!originMarker || !destinationMarker) {
        console.log('Both origin and destination required for routing');
        return;
    }
    
    const origin = originMarker.getLatLng();
    const destination = destinationMarker.getLatLng();
    
    // OSRM expects lon,lat format
    const url = `${CONFIG.osrmEndpoint}/${origin.lng},${origin.lat};${destination.lng},${destination.lat}?overview=full&geometries=geojson`;
    
    console.log('Calculating route...');
    showNotification('Calculating route...', 'info');
    
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`OSRM API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.code !== 'Ok' || !data.routes || data.routes.length === 0) {
            throw new Error('No route found');
        }
        
        const route = data.routes[0];
        currentRoute = route;
        
        // Extract route information
        const distanceMeters = route.distance;
        const distanceKm = (distanceMeters / 1000).toFixed(2);
        const durationSeconds = route.duration;
        const geometry = route.geometry;
        
        console.log(`Route calculated: ${distanceKm} km, ${Math.round(durationSeconds / 60)} minutes`);
        
        // Update distance field
        document.getElementById('distance').value = distanceKm;
        
        // Draw route on map
        drawRoute(geometry);
        
        showNotification(`Route calculated: ${distanceKm} km`, 'success');
        
    } catch (error) {
        console.error('Route calculation error:', error);
        showError('Failed to calculate route. Please check your internet connection or try different locations.');
    }
}

/**
 * Draw route polyline on map
 * @param {object} geometry - GeoJSON geometry object
 */
function drawRoute(geometry) {
    // Remove existing route line
    if (routeLine) {
        map.removeLayer(routeLine);
    }
    
    // Convert GeoJSON coordinates to Leaflet LatLng format
    const latLngs = geometry.coordinates.map(coord => [coord[1], coord[0]]);
    
    // Create polyline
    routeLine = L.polyline(latLngs, {
        color: '#2563eb',
        weight: 5,
        opacity: 0.7,
        lineJoin: 'round'
    }).addTo(map);
    
    // Fit map bounds to show entire route
    map.fitBounds(routeLine.getBounds(), {
        padding: [50, 50]
    });
}

// ============================================
// Fare Prediction
// ============================================

/**
 * Handle fare prediction form submission
 */
async function handlePrediction(e) {
    e.preventDefault();
    
    // Hide previous results/errors
    document.getElementById('predictionResult').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    
    // Validate distance is set
    const distance = document.getElementById('distance').value;
    if (!distance) {
        showError('Please set origin and destination to calculate distance first.');
        return;
    }
    
    // Collect form data
    const formData = {
        Distance_km: parseFloat(distance),
        Fuel_Price: document.getElementById('fuelPrice').value,
        Time_of_Day: document.getElementById('timeOfDay').value,
        Weather: document.getElementById('weather').value,
        Vehicle_Type: document.getElementById('vehicleType').value
    };
    
    // Validate all fields are filled
    for (const [key, value] of Object.entries(formData)) {
        if (value === '' || value === null || value === undefined) {
            showError(`Please fill in all fields. Missing: ${key.replace('_', ' ')}`);
            return;
        }
    }
    
    console.log('Prediction data:', formData);
    
    // Show loading state
    const predictBtn = document.getElementById('predictBtn');
    const btnText = predictBtn.querySelector('.btn-text');
    const spinner = predictBtn.querySelector('.spinner');
    
    predictBtn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    
    try {
        // Call backend API
        const response = await fetch(CONFIG.backendAPI, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API error: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.predicted_fare) {
            throw new Error('Invalid response from server');
        }
        
        // Display prediction result
        displayPrediction(result.predicted_fare);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Check if it's a network error
        if (error.message.includes('fetch')) {
            showError('Cannot connect to prediction server. Please ensure the backend is running. See README for setup instructions.');
        } else {
            showError(`Prediction failed: ${error.message}`);
        }
    } finally {
        // Reset button state
        predictBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

/**
 * Display prediction result
 * @param {number} fare - Predicted fare amount
 */
function displayPrediction(fare) {
    const resultDiv = document.getElementById('predictionResult');
    const fareAmount = document.getElementById('fareAmount');
    
    fareAmount.textContent = `₱${fare.toFixed(2)}`;
    resultDiv.style.display = 'block';
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    console.log(`Prediction displayed: ₱${fare.toFixed(2)}`);
}

/**
 * Display error message
 * @param {string} message - Error message
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show notification (simple alert-based, can be enhanced)
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, info, error)
 */
function showNotification(message, type = 'info') {
    // Simple console log for now
    // Can be enhanced with toast notifications
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// ============================================
// UI Controls
// ============================================

/**
 * Handle "Change Origin" button click
 */
function handleChangeOrigin() {
    if (!isSettingOrigin) {
        isSettingOrigin = true;
        document.getElementById('changeOriginBtn').textContent = '📍 Click map to set origin...';
        showNotification('Click on the map to set a new origin point', 'info');
    } else {
        isSettingOrigin = false;
        document.getElementById('changeOriginBtn').textContent = '📍 Change Origin Point';
    }
}

/**
 * Handle "Reset" button click
 */
function handleReset() {
    // Remove destination marker
    if (destinationMarker) {
        map.removeLayer(destinationMarker);
        destinationMarker = null;
    }
    
    // Remove route line
    if (routeLine) {
        map.removeLayer(routeLine);
        routeLine = null;
    }
    
    currentRoute = null;
    
    // Clear destination coordinates
    document.getElementById('destCoords').textContent = 'Not set';
    
    // Clear distance field
    document.getElementById('distance').value = '';
    
    // Hide prediction result
    document.getElementById('predictionResult').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    
    // Reset form
    document.getElementById('fareForm').reset();
    
    // Center map on origin if exists
    if (originMarker) {
        map.setView(originMarker.getLatLng(), CONFIG.defaultZoom);
    }
    
    console.log('Route reset');
    showNotification('Route cleared', 'info');
}

// ============================================
// Event Listeners
// ============================================

/**
 * Set up all event listeners
 */
function setupEventListeners() {
    // Form submission
    document.getElementById('fareForm').addEventListener('submit', handlePrediction);
    
    // Change origin button
    document.getElementById('changeOriginBtn').addEventListener('click', handleChangeOrigin);
    
    // Reset button
    document.getElementById('resetBtn').addEventListener('click', handleReset);
    
    console.log('Event listeners initialized');
}

// ============================================
// Initialization
// ============================================

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('Initializing Tricycle Fare Optimizer...');
    
    // Initialize map
    initializeMap();
    
    // Set up event listeners
    setupEventListeners();
    
    // Detect user location
    detectUserLocation();
    
    console.log('Application initialized successfully');
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
