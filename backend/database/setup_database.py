#!/usr/bin/env python3
"""
Setup SQLite database for climate data
Creates database schema and imports processed data
"""

import sqlite3
import pandas as pd
import json
import os

# Database file path
DB_PATH = '/home/ubuntu/climate_app/backend/database/climate_data.db'

# Processed data paths
ANNUAL_DATA_PATH = '/home/ubuntu/climate_app/data/processed/annual_temperatures.csv'
TRENDS_PATH = '/home/ubuntu/climate_app/data/processed/temperature_trends.json'
DECADAL_PATH = '/home/ubuntu/climate_app/data/processed/decadal_averages.json'

def create_database():
    """Create the SQLite database and tables"""
    print(f"Creating database at {DB_PATH}...")
    
    # Connect to database (will create it if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    # Annual temperature data table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS annual_temperatures (
        year INTEGER PRIMARY KEY,
        anomaly REAL NOT NULL,
        moving_avg_5yr REAL
    )
    ''')
    
    # Decadal averages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS decadal_averages (
        decade TEXT PRIMARY KEY,
        average REAL NOT NULL
    )
    ''')
    
    # Temperature trends and statistics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS temperature_trends (
        id INTEGER PRIMARY KEY,
        start_year INTEGER NOT NULL,
        end_year INTEGER NOT NULL,
        trend_per_decade REAL NOT NULL,
        warming_since_preindustrial REAL NOT NULL,
        pre_industrial_avg REAL NOT NULL,
        early_20th_century_avg REAL NOT NULL,
        late_20th_century_avg REAL NOT NULL,
        twentyfirst_century_avg REAL NOT NULL,
        warmest_year INTEGER NOT NULL,
        warmest_year_anomaly REAL NOT NULL,
        coldest_year INTEGER NOT NULL,
        coldest_year_anomaly REAL NOT NULL
    )
    ''')
    
    conn.commit()
    return conn

def import_annual_data(conn):
    """Import annual temperature data from CSV"""
    print(f"Importing annual temperature data from {ANNUAL_DATA_PATH}...")
    
    # Read CSV file
    df = pd.read_csv(ANNUAL_DATA_PATH)
    
    # Insert data into the database
    df.to_sql('annual_temperatures', conn, if_exists='replace', index=False)
    
    print(f"Imported {len(df)} annual temperature records")

def import_trends_data(conn):
    """Import temperature trends data from JSON"""
    print(f"Importing temperature trends data from {TRENDS_PATH}...")
    
    # Read JSON file
    with open(TRENDS_PATH, 'r') as f:
        trends = json.load(f)
    
    # Extract data
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO temperature_trends (
        id, start_year, end_year, trend_per_decade, warming_since_preindustrial,
        pre_industrial_avg, early_20th_century_avg, late_20th_century_avg, 
        twentyfirst_century_avg, warmest_year, warmest_year_anomaly,
        coldest_year, coldest_year_anomaly
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        1,  # id (only one record)
        trends['data_range']['start_year'],
        trends['data_range']['end_year'],
        trends['trend_per_decade'],
        trends['warming_since_preindustrial'],
        trends['average_anomalies']['pre_industrial'],
        trends['average_anomalies']['early_20th_century'],
        trends['average_anomalies']['late_20th_century'],
        trends['average_anomalies']['21st_century'],
        trends['extremes']['warmest_year']['year'],
        trends['extremes']['warmest_year']['anomaly'],
        trends['extremes']['coldest_year']['year'],
        trends['extremes']['coldest_year']['anomaly']
    ))
    
    conn.commit()
    print("Imported temperature trends data")

def import_decadal_data(conn):
    """Import decadal averages data from JSON"""
    print(f"Importing decadal averages data from {DECADAL_PATH}...")
    
    # Read JSON file
    with open(DECADAL_PATH, 'r') as f:
        decadal_data = json.load(f)
    
    # Extract data
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM decadal_averages')
    
    # Insert new data
    for decade, avg in zip(decadal_data['decades'], decadal_data['averages']):
        cursor.execute('''
        INSERT INTO decadal_averages (decade, average)
        VALUES (?, ?)
        ''', (decade, avg))
    
    conn.commit()
    print(f"Imported {len(decadal_data['decades'])} decadal average records")

def verify_database(conn):
    """Verify that data was imported correctly"""
    print("Verifying database...")
    
    cursor = conn.cursor()
    
    # Check annual data
    cursor.execute('SELECT COUNT(*) FROM annual_temperatures')
    annual_count = cursor.fetchone()[0]
    print(f"Annual temperature records: {annual_count}")
    
    # Check trends data
    cursor.execute('SELECT COUNT(*) FROM temperature_trends')
    trends_count = cursor.fetchone()[0]
    print(f"Temperature trends records: {trends_count}")
    
    # Check decadal data
    cursor.execute('SELECT COUNT(*) FROM decadal_averages')
    decadal_count = cursor.fetchone()[0]
    print(f"Decadal average records: {decadal_count}")
    
    # Sample queries
    print("\nSample data:")
    
    # Latest 5 years
    cursor.execute('''
    SELECT year, anomaly, moving_avg_5yr 
    FROM annual_temperatures 
    ORDER BY year DESC LIMIT 5
    ''')
    print("\nLatest 5 years of temperature data:")
    for row in cursor.fetchall():
        year, anomaly, moving_avg = row
        if moving_avg is not None:
            print(f"Year: {year}, Anomaly: {anomaly:.4f}°C, 5-yr Avg: {moving_avg:.4f}°C")
        else:
            print(f"Year: {year}, Anomaly: {anomaly:.4f}°C, 5-yr Avg: N/A")
    
    # Trend data
    cursor.execute('SELECT * FROM temperature_trends')
    trend = cursor.fetchone()
    print("\nTemperature trend summary:")
    print(f"Data range: {trend[1]}-{trend[2]}")
    print(f"Trend per decade: {trend[3]:.4f}°C")
    print(f"Warming since pre-industrial: {trend[4]:.4f}°C")
    print(f"Warmest year: {trend[9]} ({trend[10]:.4f}°C)")
    print(f"Coldest year: {trend[11]} ({trend[12]:.4f}°C)")

def main():
    """Main function to set up the database"""
    print("Setting up climate data database...")
    
    # Create database and tables
    conn = create_database()
    
    # Import data
    import_annual_data(conn)
    import_trends_data(conn)
    import_decadal_data(conn)
    
    # Verify database
    verify_database(conn)
    
    # Close connection
    conn.close()
    
    print(f"\nDatabase setup complete. Database file: {DB_PATH}")

if __name__ == "__main__":
    main()
