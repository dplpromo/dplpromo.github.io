// Updated configuration settings for the Climate Data Visualization app

const CONFIG = {
    // API endpoints - updated to use the exposed port URL
    API_BASE_URL: 'https://5000-i6etcfawadvnszj3d1721-75205c71.manus.computer',
    ENDPOINTS: {
        ANNUAL: '/api/annual',
        TRENDS: '/api/trends',
        DECADES: '/api/decades',
        RANGE: '/api/range'
    },
    
    // Chart colors
    COLORS: {
        ANNUAL: 'rgba(54, 162, 235, 0.5)',
        ANNUAL_BORDER: 'rgba(54, 162, 235, 1)',
        MOVING_AVG: 'rgba(255, 99, 132, 1)',
        TREND_LINE: 'rgba(75, 192, 75, 0.8)',
        DECADAL: 'rgba(153, 102, 255, 0.7)',
        DECADAL_BORDER: 'rgba(153, 102, 255, 1)',
        CUSTOM_RANGE: 'rgba(255, 159, 64, 0.7)',
        CUSTOM_RANGE_BORDER: 'rgba(255, 159, 64, 1)',
        ZERO_LINE: 'rgba(0, 0, 0, 0.2)'
    },
    
    // Chart options
    CHART_OPTIONS: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false
            },
            legend: {
                position: 'top',
            }
        }
    }
};
