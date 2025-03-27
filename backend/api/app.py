#!/usr/bin/env python3
"""
Climate Data Visualization API Server
Flask backend to serve climate data from SQLite database
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json

# Database path
DB_PATH = '/home/ubuntu/climate_app/backend/database/climate_data.db'

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'Climate Data Visualization API',
        'description': 'API for accessing global temperature data',
        'endpoints': [
            {'path': '/api/annual', 'description': 'Annual temperature anomalies'},
            {'path': '/api/trends', 'description': 'Temperature trends and statistics'},
            {'path': '/api/decades', 'description': 'Decadal temperature averages'},
            {'path': '/api/range?start=YYYY&end=YYYY', 'description': 'Temperature data for specific year range'}
        ]
    })

@app.route('/api/annual')
def annual_data():
    """Return all annual temperature data"""
    conn = get_db_connection()
    annual_temps = conn.execute('SELECT * FROM annual_temperatures ORDER BY year').fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    result = []
    for row in annual_temps:
        result.append({
            'year': row['year'],
            'anomaly': row['anomaly'],
            'moving_avg_5yr': row['moving_avg_5yr']
        })
    
    return jsonify(result)

@app.route('/api/trends')
def trends_data():
    """Return temperature trends and statistics"""
    conn = get_db_connection()
    trends = conn.execute('SELECT * FROM temperature_trends').fetchone()
    conn.close()
    
    if not trends:
        return jsonify({'error': 'No trends data found'}), 404
    
    # Convert to dictionary
    result = {
        'data_range': {
            'start_year': trends['start_year'],
            'end_year': trends['end_year']
        },
        'trend_per_decade': trends['trend_per_decade'],
        'warming_since_preindustrial': trends['warming_since_preindustrial'],
        'average_anomalies': {
            'pre_industrial': trends['pre_industrial_avg'],
            'early_20th_century': trends['early_20th_century_avg'],
            'late_20th_century': trends['late_20th_century_avg'],
            '21st_century': trends['twentyfirst_century_avg']
        },
        'extremes': {
            'warmest_year': {
                'year': trends['warmest_year'],
                'anomaly': trends['warmest_year_anomaly']
            },
            'coldest_year': {
                'year': trends['coldest_year'],
                'anomaly': trends['coldest_year_anomaly']
            }
        }
    }
    
    return jsonify(result)

@app.route('/api/decades')
def decades_data():
    """Return decadal temperature averages"""
    conn = get_db_connection()
    decades = conn.execute('SELECT * FROM decadal_averages ORDER BY decade').fetchall()
    conn.close()
    
    # Convert to dictionary with lists
    decades_list = []
    averages_list = []
    
    for row in decades:
        decades_list.append(row['decade'])
        averages_list.append(row['average'])
    
    result = {
        'decades': decades_list,
        'averages': averages_list
    }
    
    return jsonify(result)

@app.route('/api/range')
def range_data():
    """Return temperature data for a specific year range"""
    start_year = request.args.get('start', type=int)
    end_year = request.args.get('end', type=int)
    
    if not start_year or not end_year:
        return jsonify({'error': 'Missing start or end year parameter'}), 400
    
    conn = get_db_connection()
    annual_temps = conn.execute(
        'SELECT * FROM annual_temperatures WHERE year >= ? AND year <= ? ORDER BY year',
        (start_year, end_year)
    ).fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    result = []
    for row in annual_temps:
        result.append({
            'year': row['year'],
            'anomaly': row['anomaly'],
            'moving_avg_5yr': row['moving_avg_5yr']
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
