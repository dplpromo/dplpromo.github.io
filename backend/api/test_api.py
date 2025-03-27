#!/usr/bin/env python3
"""
Test script for the Climate Data API
Tests all endpoints to ensure they return the expected data
"""

import requests
import json
import time
import subprocess
import sys
import os
import signal
from threading import Thread

# API base URL
BASE_URL = 'http://localhost:5000'

def start_api_server():
    """Start the Flask API server in a separate process"""
    print("Starting API server...")
    api_process = subprocess.Popen(
        ['python3', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/home/ubuntu/climate_app/backend/api'
    )
    
    # Wait for server to start
    time.sleep(2)
    return api_process

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("✓ Root endpoint returned 200 OK")
        data = response.json()
        print(f"API name: {data.get('name')}")
        print(f"Available endpoints: {len(data.get('endpoints', []))}")
        return True
    else:
        print(f"✗ Root endpoint failed with status code {response.status_code}")
        return False

def test_annual_endpoint():
    """Test the annual data endpoint"""
    print("\nTesting annual data endpoint...")
    response = requests.get(f"{BASE_URL}/api/annual")
    
    if response.status_code == 200:
        print("✓ Annual data endpoint returned 200 OK")
        data = response.json()
        print(f"Number of annual records: {len(data)}")
        print(f"First year: {data[0]['year']}")
        print(f"Last year: {data[-1]['year']}")
        return True
    else:
        print(f"✗ Annual data endpoint failed with status code {response.status_code}")
        return False

def test_trends_endpoint():
    """Test the trends data endpoint"""
    print("\nTesting trends data endpoint...")
    response = requests.get(f"{BASE_URL}/api/trends")
    
    if response.status_code == 200:
        print("✓ Trends data endpoint returned 200 OK")
        data = response.json()
        print(f"Data range: {data['data_range']['start_year']} to {data['data_range']['end_year']}")
        print(f"Trend per decade: {data['trend_per_decade']}°C")
        print(f"Warmest year: {data['extremes']['warmest_year']['year']} ({data['extremes']['warmest_year']['anomaly']}°C)")
        return True
    else:
        print(f"✗ Trends data endpoint failed with status code {response.status_code}")
        return False

def test_decades_endpoint():
    """Test the decades data endpoint"""
    print("\nTesting decades data endpoint...")
    response = requests.get(f"{BASE_URL}/api/decades")
    
    if response.status_code == 200:
        print("✓ Decades data endpoint returned 200 OK")
        data = response.json()
        print(f"Number of decades: {len(data['decades'])}")
        print(f"Decades: {', '.join(data['decades'][:5])}...")
        return True
    else:
        print(f"✗ Decades data endpoint failed with status code {response.status_code}")
        return False

def test_range_endpoint():
    """Test the range data endpoint"""
    print("\nTesting range data endpoint...")
    start_year = 2000
    end_year = 2020
    response = requests.get(f"{BASE_URL}/api/range?start={start_year}&end={end_year}")
    
    if response.status_code == 200:
        print(f"✓ Range data endpoint returned 200 OK for years {start_year}-{end_year}")
        data = response.json()
        print(f"Number of records: {len(data)}")
        print(f"Years included: {data[0]['year']} to {data[-1]['year']}")
        return True
    else:
        print(f"✗ Range data endpoint failed with status code {response.status_code}")
        return False

def main():
    """Main test function"""
    print("Testing Climate Data API...")
    
    # Start the API server
    api_process = start_api_server()
    
    try:
        # Run all tests
        tests = [
            test_root_endpoint,
            test_annual_endpoint,
            test_trends_endpoint,
            test_decades_endpoint,
            test_range_endpoint
        ]
        
        results = []
        for test in tests:
            results.append(test())
        
        # Print summary
        print("\nTest Summary:")
        print(f"Total tests: {len(tests)}")
        print(f"Passed: {results.count(True)}")
        print(f"Failed: {results.count(False)}")
        
        if all(results):
            print("\n✓ All tests passed! The API is working correctly.")
        else:
            print("\n✗ Some tests failed. Please check the API implementation.")
    
    finally:
        # Stop the API server
        print("\nStopping API server...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    main()
