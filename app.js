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
    // Backend API endpoint - relative path for Firebase (proxied via rewrites) or localhost for development.
    // To host the backend on Hugging Face Spaces, set useHuggingFace to true and provide huggingFaceEndpoint.
    useHuggingFace: true,
    huggingFaceEndpoint: 'https://semiautomat1c-tagum-tricycle-fare-backend.hf.space/api/predict',

    get backendAPI() {
        if (this.useHuggingFace && this.huggingFaceEndpoint && !this.huggingFaceEndpoint.includes('<your-username>')) {
            return this.huggingFaceEndpoint;
        }
        return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://127.0.0.1:5001/api/predict'
            : '/api/predict';
    }
};

// Global state
let map;
let originMarker = null;
let destinationMarker = null;
let routeLine = null;
let currentRoute = null;
let isSettingOrigin = false;
let availableRoutes = []; // Store all available route alternatives
let routeLines = []; // Store all route polylines for visualization
let routeCasingLines = []; // White casing beneath the selected route for map contrast
let selectedRouteIndex = 0; // Currently selected route index
let toastTimer = null;
let routeRequestVersion = 0;
let predictionRequestVersion = 0;
let mapResizeTimer = null;

const ICONS = {
    pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s6-5.1 6-11a6 6 0 1 0-12 0c0 5.9 6 11 6 11Z"></path><circle cx="12" cy="10" r="2"></circle></svg>',
    search: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"></circle><path d="m16 16 4 4"></path></svg>',
    distance: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"></path><path d="m13 6 6 6-6 6"></path></svg>',
    clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path></svg>'
};

function setElementHidden(element, hidden) {
    if (!element) return;
    element.hidden = hidden;
}

function setSearchExpanded(expanded) {
    const searchInput = document.getElementById('destinationSearch');
    if (searchInput) {
        searchInput.setAttribute('aria-expanded', String(expanded));
    }
}

function showStatus(message, type = 'info') {
    const status = document.getElementById('statusMessage');
    if (!status) return;

    status.textContent = message;
    status.dataset.type = type;
    status.hidden = false;
}

function clearStatus() {
    const status = document.getElementById('statusMessage');
    if (!status) return;

    status.textContent = '';
    status.hidden = true;
    delete status.dataset.type;
}

function showToast(message, type = 'info') {
    const region = document.getElementById('toastRegion');
    if (!region) return;

    region.replaceChildren();
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.dataset.type = type;
    toast.textContent = message;
    region.appendChild(toast);

    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => {
        toast.remove();
    }, 3600);
}

function setSheetExpanded(expanded) {
    const sheet = document.getElementById('estimatorSheet');
    const toggle = document.getElementById('sheetToggle');
    if (!sheet || !toggle) return;

    sheet.classList.toggle('is-expanded', expanded);
    toggle.setAttribute('aria-expanded', String(expanded));
}

function clearSearchSuggestions() {
    const suggestions = document.getElementById('searchSuggestions');
    if (!suggestions) return;

    suggestions.replaceChildren();
    suggestions.hidden = true;
    setSearchExpanded(false);
}

// Popular destinations in Tagum City with accurate coordinates
const DESTINATIONS = [
    { name: 'Gaisano Mall of Tagum', category: 'Shopping', lat: 7.448802, lng: 125.811507 },
    { name: 'Tagum City Hall', category: 'Government', lat: 7.440798, lng: 125.826451 },
    { name: 'Robinsons Place Tagum', category: 'Shopping', lat: 7.430195, lng: 125.796646 },
    { name: 'UM Tagum College - Visayan', category: 'Education', lat: 7.426032, lng: 125.793776 },
    { name: 'Energy Park', category: 'Recreational', lat: 7.415599, lng: 125.826301 },
    { name: 'UM Tagum College - Arellano', category: 'Education', lat: 7.446727, lng: 125.801287 },
    { name: 'Tagum Public Market', category: 'Market', lat: 7.461004, lng: 125.801672 },
    { name: 'Tagum Terminal', category: 'Transportation', lat: 7.461214, lng: 125.798928 },
    { name: 'NCCC Mall Tagum', category: 'Shopping', lat: 7.451530, lng: 125.813445 },
    { name: 'Tagum City Historical and Cultural Center', category: 'Landmark', lat: 7.447796, lng: 125.804273 },
    { name: 'Tagum Doctors\' Hospital', category: 'Healthcare', lat: 7.439006, lng: 125.803606 },
    { name: 'Big 8 Corporate Hotel', category: 'Hotel', lat: 7.441489, lng: 125.805756 },
    { name: 'St. Mary\'s College of Tagum', category: 'Education', lat: 7.454189, lng: 125.815612 }
];

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

    // Leaflet needs an explicit size refresh when the responsive workspace changes.
    const mapContainer = document.getElementById('map');
    new ResizeObserver(() => {
        window.clearTimeout(mapResizeTimer);
        mapResizeTimer = window.setTimeout(() => {
            map.invalidateSize();
            fitSelectedRoute();
        }, 120);
    }).observe(mapContainer);

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
        updateOriginButton(false);
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
        showStatus('Finding your current location...', 'info');

        navigator.geolocation.getCurrentPosition(
            // Success callback
            (position) => {
                const { latitude, longitude } = position.coords;
                console.log(`Location detected: ${latitude}, ${longitude}`);

                setOrigin(latitude, longitude);
                map.setView([latitude, longitude], CONFIG.defaultZoom);

                showNotification('Current location set as your origin.', 'success');
            },
            // Error callback
            (error) => {
                console.info('Geolocation unavailable:', error.message);

                let message = 'Location access denied. ';
                switch (error.code) {
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

                // Default to Tagum City center
                setOrigin(CONFIG.tagumCity.lat, CONFIG.tagumCity.lng);
                showStatus(`${message} Tagum City center is set as your origin.`, 'info');
                showToast('Using Tagum City center as your origin.', 'info');
            },
            // Options
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        showStatus('Location detection is not supported by this browser. Tagum City center is set as your origin.', 'info');
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
    originMarker.on('dragend', function (e) {
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
 * @param {string} name - Optional destination name
 */
function setDestination(lat, lng, name = null) {
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
        title: name || 'Destination'
    }).addTo(map);

    const popupText = name ? `<b>${name}</b>` : '<b>Destination</b>';
    destinationMarker.bindPopup(popupText).openPopup();

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
 * Calculate route using OSRM API with alternatives
 */
async function calculateRoute() {
    if (!originMarker || !destinationMarker) {
        console.log('Both origin and destination required for routing');
        return;
    }

    const origin = originMarker.getLatLng();
    const destination = destinationMarker.getLatLng();
    const requestVersion = ++routeRequestVersion;

    // OSRM expects lon,lat format - request alternative routes
    const url = `${CONFIG.osrmEndpoint}/${origin.lng},${origin.lat};${destination.lng},${destination.lat}?overview=full&geometries=geojson&alternatives=true`;

    console.log('Calculating routes...');
    showStatus('Calculating available routes...', 'info');

    try {
        const response = await fetch(url);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Details:', errorText);
            try {
                const errorJson = JSON.parse(errorText);
                if (errorJson.path) {
                    console.error('Debug - Path received by server:', errorJson.path);
                    console.error('Debug - Method received by server:', errorJson.method);
                }
            } catch (e) {
                // Not JSON
            }
            throw new Error(`API error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();

        if (requestVersion !== routeRequestVersion) {
            return;
        }

        if (data.code !== 'Ok' || !data.routes || data.routes.length === 0) {
            throw new Error('No route found');
        }

        // Store all available routes
        availableRoutes = data.routes;
        selectedRouteIndex = 0;
        currentRoute = availableRoutes[0];

        console.log(`Found ${availableRoutes.length} route(s)`);
        console.log('Route data:', data.routes.map((r, i) => ({
            route: i + 1,
            distance: (r.distance / 1000).toFixed(2) + ' km',
            duration: Math.round(r.duration / 60) + ' min'
        })));

        // Display all routes on map
        displayAllRoutes();

        // Update route selector UI
        updateRouteSelector();

        // Update distance field with selected route
        updateSelectedRoute(0);

        if (availableRoutes.length > 1) {
            showNotification(`${availableRoutes.length} routes found. Select the route you want to estimate.`, 'success');
        } else {
            showNotification('Route calculated. Add the current trip conditions to estimate your fare.', 'success');
        }

        setSheetExpanded(true);

    } catch (error) {
        console.error('Route calculation error:', error);
        showError('Failed to calculate route. Please check your internet connection or try different locations.');
    }
}

/**
 * Display all available routes on the map
 */
function displayAllRoutes() {
    // Remove existing route lines
    routeLines.forEach(line => map.removeLayer(line));
    routeLines = [];
    routeCasingLines.forEach(line => map.removeLayer(line));
    routeCasingLines = [];

    if (routeLine) {
        map.removeLayer(routeLine);
        routeLine = null;
    }

    // Draw all routes
    availableRoutes.forEach((route, index) => {
        const latLngs = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);

        // Different styling for selected vs alternative routes
        const isSelected = index === selectedRouteIndex;
        const casing = L.polyline(latLngs, {
            color: '#ffffff',
            weight: 11,
            opacity: isSelected ? 0.96 : 0,
            interactive: false,
            lineJoin: 'round'
        }).addTo(map);
        const polyline = L.polyline(latLngs, {
            color: isSelected ? '#0369a1' : '#64748b',
            weight: isSelected ? 7 : 4,
            opacity: isSelected ? 1 : 0.58,
            lineJoin: 'round'
        }).addTo(map);
        polyline.getElement()?.classList.toggle('is-selected-route', isSelected);

        // Add click handler to select route
        polyline.on('click', () => selectRoute(index));

        routeCasingLines.push(casing);
        routeLines.push(polyline);
    });

    fitSelectedRoute();
}

function fitSelectedRoute() {
    if (!map || !routeLines[selectedRouteIndex]) return;

    map.fitBounds(routeLines[selectedRouteIndex].getBounds(), {
        padding: [32, 32],
        maxZoom: 16
    });
}

/**
 * Select a specific route by index
 * @param {number} index - Route index to select
 */
function selectRoute(index) {
    if (index < 0 || index >= availableRoutes.length) return;

    selectedRouteIndex = index;
    currentRoute = availableRoutes[index];

    // Update route visualization
    routeLines.forEach((line, i) => {
        const isSelected = i === index;
        routeCasingLines[i].setStyle({
            opacity: isSelected ? 0.96 : 0
        });
        line.setStyle({
            color: isSelected ? '#0369a1' : '#64748b',
            weight: isSelected ? 7 : 4,
            opacity: isSelected ? 1 : 0.58
        });
        line.getElement()?.classList.toggle('is-selected-route', isSelected);

        // Bring selected route to front
        if (isSelected) {
            line.bringToFront();
        }
    });

    // Update UI
    updateSelectedRoute(index);
    updateRouteSelector();
    fitSelectedRoute();
}

/**
 * Update the selected route information
 * @param {number} index - Route index
 */
function updateSelectedRoute(index) {
    const route = availableRoutes[index];
    const distanceKm = (route.distance / 1000).toFixed(2);

    // Update distance field
    document.getElementById('distance').value = distanceKm;

    console.log(`Route ${index + 1} selected: ${distanceKm} km, ${Math.round(route.duration / 60)} minutes`);
}

/**
 * Update the route selector UI with available routes
 */
function updateRouteSelector() {
    const container = document.getElementById('routeOptionsContainer');
    if (!container) return;

    // Clear existing options
    container.replaceChildren();

    // Hide if only one route
    if (availableRoutes.length <= 1) {
        container.hidden = true;
        return;
    }

    container.hidden = false;

    const title = document.createElement('h3');
    title.className = 'route-options-title';
    title.textContent = 'Available routes';
    container.appendChild(title);

    // Create route option cards
    availableRoutes.forEach((route, index) => {
        const distanceKm = (route.distance / 1000).toFixed(2);
        const durationMin = Math.round(route.duration / 60);
        const isSelected = index === selectedRouteIndex;

        const optionCard = document.createElement('button');
        optionCard.type = 'button';
        optionCard.className = `route-option ${isSelected ? 'selected' : ''}`;
        optionCard.setAttribute('aria-pressed', String(isSelected));
        optionCard.innerHTML = `
            <div class="route-option-header">
                <span class="route-option-title">Route ${index + 1}</span>
                ${isSelected ? '<span class="route-badge">Selected</span>' : ''}
            </div>
            <div class="route-option-details">
                <div class="route-detail">
                    ${ICONS.distance}
                    <span>${distanceKm} km</span>
                </div>
                <div class="route-detail">
                    ${ICONS.clock}
                    <span>${durationMin} min</span>
                </div>
            </div>
        `;

        optionCard.addEventListener('click', () => selectRoute(index));
        container.appendChild(optionCard);
    });
}

/**
 * Draw route polyline on map (legacy function for compatibility)
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
    setElementHidden(document.getElementById('predictionResult'), true);
    setElementHidden(document.getElementById('errorMessage'), true);

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
    btnText.hidden = true;
    spinner.hidden = false;
    showStatus('Calculating your fare estimate...', 'info');
    const requestVersion = ++predictionRequestVersion;

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
            const errorText = await response.text();
            console.error('API Error Details:', errorText);
            try {
                const errorJson = JSON.parse(errorText);
                if (errorJson.path) {
                    console.error('Debug - Path received by server:', errorJson.path);
                }
                throw new Error(errorJson.error || `API error: ${response.status}`);
            } catch (e) {
                // Not JSON or parsing failed
                throw new Error(`API error: ${response.status} - ${errorText.substring(0, 100)}`);
            }
        }

        const result = await response.json();

        if (requestVersion !== predictionRequestVersion) {
            return;
        }

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
        if (requestVersion !== predictionRequestVersion) {
            return;
        }

        // Reset button state
        predictBtn.disabled = false;
        btnText.hidden = false;
        spinner.hidden = true;
    }
}

/**
 * Display prediction result
 * @param {number} fare - Predicted fare amount
 */
function displayPrediction(fare) {
    const resultDiv = document.getElementById('predictionResult');
    const fareAmount = document.getElementById('fareAmount');

    // Display as whole number (no decimals for tricycle fares)
    fareAmount.textContent = `₱${Math.round(fare)}`;
    resultDiv.hidden = false;
    clearStatus();
    showToast('Fare estimate ready.', 'success');

    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    resultDiv.focus({ preventScroll: true });

    console.log(`Prediction displayed: ₱${Math.round(fare)}`);
}

/**
 * Display error message
 * @param {string} message - Error message
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.hidden = false;
    showToast(message, 'error');

    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show notification (simple alert-based, can be enhanced)
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, info, error)
 */
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    showStatus(message, type);
    showToast(message, type);
}

// ============================================
// Destination Search
// ============================================

/**
 * Filter and display destination suggestions based on search input
 * @param {string} searchText - User's search input
 */
async function filterDestinations(searchText) {
    const suggestionsContainer = document.getElementById('searchSuggestions');

    if (!searchText || searchText.trim().length < 2) {
        clearSearchSuggestions();
        return;
    }

    const query = searchText.toLowerCase().trim();

    // Filter destinations that match the search query
    const matches = DESTINATIONS.filter(dest =>
        dest.name.toLowerCase().includes(query) ||
        dest.category.toLowerCase().includes(query)
    );

    if (matches.length === 0) {
        // If no predefined matches, search using Nominatim
        await searchNominatim(query);
        return;
    }

    renderDestinationSuggestions(matches, ICONS.pin);
}

function renderDestinationSuggestions(destinations, icon) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    suggestionsContainer.replaceChildren();

    destinations.forEach(destination => {
        const option = document.createElement('button');
        option.type = 'button';
        option.className = 'suggestion-item';
        option.setAttribute('role', 'option');
        option.dataset.lat = destination.lat;
        option.dataset.lng = destination.lng;
        option.dataset.name = destination.name;

        const iconContainer = document.createElement('span');
        iconContainer.className = 'suggestion-icon';
        iconContainer.innerHTML = icon;

        const text = document.createElement('span');
        text.className = 'suggestion-text';

        const name = document.createElement('span');
        name.className = 'suggestion-name';
        name.textContent = destination.name;

        const category = document.createElement('span');
        category.className = 'suggestion-category';
        category.textContent = destination.category;

        text.append(name, category);
        option.append(iconContainer, text);
        option.addEventListener('click', () => {
            selectDestination(Number(destination.lat), Number(destination.lng), destination.name);
        });
        suggestionsContainer.appendChild(option);
    });

    suggestionsContainer.hidden = false;
    setSearchExpanded(true);
}

function renderSearchMessage(message) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    const status = document.createElement('div');
    status.className = 'search-empty';
    status.textContent = message;
    suggestionsContainer.replaceChildren(status);
    suggestionsContainer.hidden = false;
    setSearchExpanded(true);
}

/**
 * Search for locations using Nominatim OpenStreetMap API
 * @param {string} query - Search query
 */
async function searchNominatim(query) {
    renderSearchMessage('Searching nearby destinations...');

    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query + ', Tagum City, Philippines')}&format=json&limit=5`);
        const results = await response.json();

        if (results.length === 0) {
            renderSearchMessage('No destinations found. Try a different search or select a point on the map.');
            return;
        }

        renderDestinationSuggestions(results.map(result => ({
            lat: result.lat,
            lng: result.lon,
            name: result.display_name.split(',')[0],
            category: result.type || 'Location'
        })), ICONS.search);
    } catch (error) {
        console.error('Nominatim search error:', error);
        renderSearchMessage('Destination search is unavailable. Try again or select a point on the map.');
    }
}

/**
 * Geocode a location and set it as destination
 * @param {string} searchQuery - Location search query
 * @param {string} displayName - Display name for the location
 */
async function geocodeAndSetDestination(searchQuery, displayName) {
    const searchInput = document.getElementById('destinationSearch');
    const suggestionsContainer = document.getElementById('searchSuggestions');

    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery)}&format=json&limit=1`);
        const results = await response.json();

        if (results.length > 0) {
            const lat = parseFloat(results[0].lat);
            const lng = parseFloat(results[0].lon);

            searchInput.value = displayName;
            clearSearchSuggestions();

            setDestination(lat, lng, displayName);
            map.setView([lat, lng], 15);
        } else {
            showError('Could not find that location. Try selecting a point on the map.');
        }
    } catch (error) {
        console.error('Geocoding error:', error);
        showError('Destination search is unavailable. Try selecting a point on the map.');
    }
}

/**
 * Select a destination from search results
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude  
 * @param {string} name - Destination name
 */
function selectDestination(lat, lng, name) {
    const searchInput = document.getElementById('destinationSearch');
    // Update search input
    searchInput.value = name;

    // Hide suggestions
    clearSearchSuggestions();

    // Set destination on map
    setDestination(lat, lng, name);

    // Pan map to show destination
    map.setView([lat, lng], 15);
}

/**
 * Handle keyboard navigation in search suggestions
 * @param {KeyboardEvent} e - Keyboard event
 */
function handleSearchKeyboard(e) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    const items = suggestionsContainer.querySelectorAll('.suggestion-item[data-lat]');

    if (items.length === 0) return;

    const activeItem = suggestionsContainer.querySelector('.suggestion-item.active');
    let currentIndex = Array.from(items).indexOf(activeItem);

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (activeItem) activeItem.classList.remove('active');
        currentIndex = (currentIndex + 1) % items.length;
        items[currentIndex].classList.add('active');
        items[currentIndex].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (activeItem) activeItem.classList.remove('active');
        currentIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
        items[currentIndex].classList.add('active');
        items[currentIndex].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter') {
        e.preventDefault();
        if (activeItem) {
            activeItem.click();
        } else if (items.length > 0) {
            items[0].click();
        }
    } else if (e.key === 'Escape') {
        clearSearchSuggestions();
    }
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
        updateOriginButton(true);
        showNotification('Select a point on the map to set your origin.', 'info');
    } else {
        isSettingOrigin = false;
        updateOriginButton(false);
    }
}

function updateOriginButton(isActive) {
    const button = document.getElementById('changeOriginBtn');
    const label = document.querySelector('#changeOriginBtn span');
    if (label) {
        label.textContent = isActive ? 'Select origin on map' : 'Set origin';
    }
    button.setAttribute('aria-label', isActive ? 'Cancel origin selection' : 'Set origin');
}

/**
 * Handle "Reset" button click
 */
function handleReset() {
    routeRequestVersion += 1;
    predictionRequestVersion += 1;

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

    routeLines.forEach(line => map.removeLayer(line));
    routeLines = [];
    routeCasingLines.forEach(line => map.removeLayer(line));
    routeCasingLines = [];
    availableRoutes = [];
    selectedRouteIndex = 0;
    currentRoute = null;
    isSettingOrigin = false;
    updateOriginButton(false);

    // Clear destination coordinates
    document.getElementById('destCoords').textContent = 'Not set';

    // Clear distance field
    document.getElementById('distance').value = '';

    // Clear search input
    document.getElementById('destinationSearch').value = '';
    clearSearchSuggestions();

    // Hide prediction result
    setElementHidden(document.getElementById('predictionResult'), true);
    setElementHidden(document.getElementById('errorMessage'), true);
    const routeOptionsContainer = document.getElementById('routeOptionsContainer');
    routeOptionsContainer.replaceChildren();
    setElementHidden(routeOptionsContainer, true);
    clearStatus();

    // Reset form
    document.getElementById('fareForm').reset();
    const predictBtn = document.getElementById('predictBtn');
    predictBtn.disabled = false;
    predictBtn.querySelector('.btn-text').hidden = false;
    predictBtn.querySelector('.spinner').hidden = true;

    // Center map on origin if exists
    if (originMarker) {
        map.setView(originMarker.getLatLng(), CONFIG.defaultZoom);
    }

    console.log('Route reset');
    showNotification('Route cleared. Search for a new destination when you are ready.', 'info');
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

    document.getElementById('sheetToggle').addEventListener('click', function () {
        const sheet = document.getElementById('estimatorSheet');
        setSheetExpanded(!sheet.classList.contains('is-expanded'));
    });

    // Destination search input
    const searchInput = document.getElementById('destinationSearch');
    searchInput.addEventListener('input', function (e) {
        filterDestinations(e.target.value);
    });

    // Keyboard navigation for search
    searchInput.addEventListener('keydown', handleSearchKeyboard);

    // Hide suggestions when clicking outside
    document.addEventListener('click', function (e) {
        const searchContainer = document.querySelector('.search-container');
        if (searchContainer && !searchContainer.contains(e.target)) {
            clearSearchSuggestions();
        }
    });

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
