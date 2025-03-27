#!/bin/bash
# Startup script for Climate Data Visualization Application

# Exit on error
set -e

echo "Starting Climate Data Visualization Application..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r backend/api/requirements.txt

# Check if database exists, if not initialize it
if [ ! -f "backend/database/climate_data.db" ]; then
    echo "Initializing database..."
    cd backend/database
    python setup_database.py
    cd ../..
fi

# Start the backend API server
echo "Starting backend API server..."
cd backend/api
python app.py &
API_PID=$!
cd ../..

echo "Backend API server running with PID: $API_PID"
echo "API available at: http://localhost:5000"

# Start the frontend server
echo "Starting frontend server..."
cd frontend
python -m http.server 8000 &
FRONTEND_PID=$!
cd ..

echo "Frontend server running with PID: $FRONTEND_PID"
echo "Frontend available at: http://localhost:8000"

echo "Climate Data Visualization Application is now running!"
echo "Press Ctrl+C to stop the servers"

# Wait for user to press Ctrl+C
trap "echo 'Stopping servers...'; kill $API_PID $FRONTEND_PID; exit" INT
wait
