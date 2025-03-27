// Main application logic for Climate Data Visualization

// Global data storage
let annualData = [];
let trendsData = {};
let decadalData = {};

// DOM elements
const startYearSelect = document.getElementById('startYear');
const endYearSelect = document.getElementById('endYear');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Fetch all required data
    fetchData();
    
    // Set up event listeners
    setupEventListeners();
});

// Fetch all data from the API
async function fetchData() {
    try {
        // Fetch annual temperature data
        const annualResponse = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.ANNUAL}`);
        annualData = await annualResponse.json();
        
        // Fetch trends data
        const trendsResponse = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.TRENDS}`);
        trendsData = await trendsResponse.json();
        
        // Fetch decadal data
        const decadalResponse = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.DECADES}`);
        decadalData = await decadalResponse.json();
        
        // Initialize charts and UI
        initializeUI();
        createCharts();
        updateKeyStats();
        
    } catch (error) {
        console.error('Error fetching data:', error);
        displayErrorMessage('Failed to load climate data. Please try again later.');
    }
}

// Initialize UI elements
function initializeUI() {
    // Populate year dropdowns
    populateYearDropdowns();
}

// Create all charts
function createCharts() {
    createTemperatureChart(annualData);
    createDecadalChart(decadalData);
    
    // Initialize custom range chart with default range (last 30 years)
    const endYear = annualData[annualData.length - 1].year;
    const startYear = endYear - 30;
    
    // Set default values in dropdowns
    startYearSelect.value = startYear;
    endYearSelect.value = endYear;
    
    // Create custom range chart
    createCustomRangeChart(annualData, startYear, endYear);
}

// Update key statistics display
function updateKeyStats() {
    if (!trendsData || Object.keys(trendsData).length === 0) {
        return;
    }
    
    // Update DOM elements with trends data
    document.getElementById('dataRange').textContent = 
        `${trendsData.data_range.start_year} to ${trendsData.data_range.end_year}`;
    
    document.getElementById('trendPerDecade').textContent = 
        `${trendsData.trend_per_decade.toFixed(2)}°C`;
    
    document.getElementById('warmingSincePreindustrial').textContent = 
        `${trendsData.warming_since_preindustrial.toFixed(2)}°C`;
    
    document.getElementById('warmestYear').textContent = 
        `${trendsData.extremes.warmest_year.year} (${trendsData.extremes.warmest_year.anomaly.toFixed(2)}°C)`;
    
    document.getElementById('coldestYear').textContent = 
        `${trendsData.extremes.coldest_year.year} (${trendsData.extremes.coldest_year.anomaly.toFixed(2)}°C)`;
}

// Populate year dropdown selectors
function populateYearDropdowns() {
    if (!annualData || annualData.length === 0) {
        return;
    }
    
    // Get min and max years
    const minYear = annualData[0].year;
    const maxYear = annualData[annualData.length - 1].year;
    
    // Clear existing options
    startYearSelect.innerHTML = '';
    endYearSelect.innerHTML = '';
    
    // Add options for each year
    for (let year = minYear; year <= maxYear; year++) {
        const startOption = document.createElement('option');
        startOption.value = year;
        startOption.textContent = year;
        startYearSelect.appendChild(startOption);
        
        const endOption = document.createElement('option');
        endOption.value = year;
        endOption.textContent = year;
        endYearSelect.appendChild(endOption);
    }
}

// Set up event listeners
function setupEventListeners() {
    // Year range selection
    startYearSelect.addEventListener('change', updateCustomRangeChart);
    endYearSelect.addEventListener('change', updateCustomRangeChart);
}

// Update custom range chart based on selected years
function updateCustomRangeChart() {
    const startYear = parseInt(startYearSelect.value);
    const endYear = parseInt(endYearSelect.value);
    
    // Validate range
    if (startYear > endYear) {
        alert('Start year must be less than or equal to end year');
        return;
    }
    
    // Update chart
    createCustomRangeChart(annualData, startYear, endYear);
}

// Display error message
function displayErrorMessage(message) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
}
