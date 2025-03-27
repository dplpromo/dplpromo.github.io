# Climate Data Visualization Application

A full-stack web application for visualizing global temperature trends using the NOAA Global Surface Temperature Dataset.

## Features

- **Interactive Temperature Charts**: Visualize global temperature anomalies from 1880 to 2022
- **Trend Analysis**: View warming trends, decadal averages, and key statistics
- **Custom Range Explorer**: Select specific time periods to examine in detail
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask API server with SQLite database
- **Frontend**: HTML, CSS (Bootstrap), and JavaScript (Chart.js)
- **Data Source**: NOAA Global Surface Temperature Dataset (NOAAGlobalTemp)

## Project Structure

```
climate_app/
├── data/                  # Data files and processing scripts
│   ├── processed/         # Processed data files
│   ├── global_temp_data.asc  # Raw NOAA temperature data
│   └── process_data.py    # Data processing script
├── backend/               # Backend API server
│   ├── api/               # Flask API application
│   │   ├── app.py         # Main API server
│   │   ├── requirements.txt  # Python dependencies
│   │   └── test_api.py    # API test script
│   └── database/          # Database files
│       ├── climate_data.db  # SQLite database
│       └── setup_database.py  # Database setup script
└── frontend/              # Frontend web application
    ├── css/               # CSS stylesheets
    │   └── styles.css     # Custom styles
    ├── js/                # JavaScript files
    │   ├── app.js         # Main application logic
    │   ├── charts.js      # Chart.js implementations
    │   └── config.js      # Configuration settings
    └── index.html         # Main HTML page
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Web browser with JavaScript enabled

### Backend Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd climate_app
   ```

2. Set up a Python virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```
   cd backend/api
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   cd ../database
   python setup_database.py
   ```

5. Start the API server:
   ```
   cd ../api
   python app.py
   ```
   The API server will run on http://localhost:5000

### Frontend Setup

1. In a new terminal, navigate to the frontend directory:
   ```
   cd climate_app/frontend
   ```

2. Start a simple HTTP server:
   ```
   python -m http.server 8000
   ```
   The frontend will be available at http://localhost:8000

3. Open your web browser and navigate to http://localhost:8000

## API Endpoints

The backend provides the following API endpoints:

- **GET /** - API information and available endpoints
- **GET /api/annual** - Annual temperature anomalies from 1880 to 2022
- **GET /api/trends** - Temperature trends and statistics
- **GET /api/decades** - Decadal temperature averages
- **GET /api/range?start=YYYY&end=YYYY** - Temperature data for a specific year range

## Data Processing

The application uses the NOAA Global Surface Temperature Dataset, which provides temperature anomalies relative to the 1971-2000 baseline period. The data processing script (`process_data.py`) performs the following operations:

1. Reads the raw temperature data
2. Calculates key statistics and trends
3. Computes decadal averages and 5-year moving averages
4. Prepares the data for visualization and database storage

## Deployment

### Local Deployment

Follow the installation and setup instructions above to run the application locally.

### Production Deployment

For production deployment, consider the following options:

1. **Backend API**:
   - Deploy the Flask API using a WSGI server like Gunicorn
   - Set `debug=False` in app.py for production
   - Consider using a production-ready database like PostgreSQL

2. **Frontend**:
   - Deploy the static files to a web server or CDN
   - Update the API_BASE_URL in config.js to point to your deployed API

3. **GitHub Pages** (Frontend only):
   - The frontend can be deployed to GitHub Pages
   - The backend API would need to be hosted separately

## Future Enhancements

- Add more visualization types (e.g., heatmaps, global maps)
- Implement user authentication for saving custom views
- Add comparison with climate models and projections
- Include more climate datasets (precipitation, sea level, etc.)

## Credits

- Data source: [NOAA Global Surface Temperature Dataset](https://www.ncei.noaa.gov/products/land-based-station/noaa-global-temp)
- Built with [Flask](https://flask.palletsprojects.com/), [Bootstrap](https://getbootstrap.com/), and [Chart.js](https://www.chartjs.org/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
