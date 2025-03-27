#!/usr/bin/env python3
"""
Process NOAA Global Surface Temperature Dataset
Extracts key trends and prepares data for visualization and database storage
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# Input and output file paths
input_file = '/home/ubuntu/climate_app/data/global_temp_data.asc'
output_dir = '/home/ubuntu/climate_app/data/processed'
trends_file = os.path.join(output_dir, 'temperature_trends.json')
decadal_file = os.path.join(output_dir, 'decadal_averages.json')
annual_csv_file = os.path.join(output_dir, 'annual_temperatures.csv')
plot_file = os.path.join(output_dir, 'temperature_plot.png')

# Read the data
# Based on the readme, we know the columns are:
# 1st column = year
# 2nd column = anomaly of temperature (K)
# 3rd column = total error variance (K**2)
# 4th column = high-frequency error variance (K**2)
# 5th column = low-frequency error variance (K**2)
# 6th column = bias error variance (K**2)

print("Reading temperature data...")
df = pd.read_csv(input_file, delim_whitespace=True, header=None,
                names=['year', 'anomaly', 'total_error_var', 'high_freq_error_var', 
                       'low_freq_error_var', 'bias_error_var'])

# Basic data exploration
print(f"Data range: {df['year'].min()} to {df['year'].max()}")
print(f"Number of data points: {len(df)}")
print(f"Temperature anomaly range: {df['anomaly'].min():.4f} to {df['anomaly'].max():.4f} K")

# Calculate key statistics and trends
print("Calculating key statistics and trends...")

# Overall trend (linear regression)
x = df['year'].values
y = df['anomaly'].values
slope, intercept = np.polyfit(x, y, 1)
trend_per_decade = slope * 10  # degrees per decade

# Calculate decadal averages
df['decade'] = (df['year'] // 10) * 10
decadal_avg = df.groupby('decade')['anomaly'].mean().reset_index()
decadal_avg['decade_label'] = decadal_avg['decade'].astype(str) + 's'

# Calculate 5-year moving average for smoother trend visualization
df['moving_avg_5yr'] = df['anomaly'].rolling(window=5, center=True).mean()

# Calculate average anomalies for different periods
pre_industrial = df[df['year'] < 1900]['anomaly'].mean()
early_20th = df[(df['year'] >= 1900) & (df['year'] < 1950)]['anomaly'].mean()
late_20th = df[(df['year'] >= 1950) & (df['year'] < 2000)]['anomaly'].mean()
recent = df[df['year'] >= 2000]['anomaly'].mean()

# Calculate warming since pre-industrial times
warming_since_preindustrial = recent - pre_industrial

# Find the warmest and coldest years
warmest_year = df.loc[df['anomaly'].idxmax()]
coldest_year = df.loc[df['anomaly'].idxmin()]

# Prepare data for visualization and API
print("Preparing data for visualization and API...")

# Create a summary of key trends
trends_summary = {
    "data_range": {
        "start_year": int(df['year'].min()),
        "end_year": int(df['year'].max())
    },
    "trend_per_decade": float(f"{trend_per_decade:.4f}"),
    "warming_since_preindustrial": float(f"{warming_since_preindustrial:.4f}"),
    "average_anomalies": {
        "pre_industrial": float(f"{pre_industrial:.4f}"),
        "early_20th_century": float(f"{early_20th:.4f}"),
        "late_20th_century": float(f"{late_20th:.4f}"),
        "21st_century": float(f"{recent:.4f}")
    },
    "extremes": {
        "warmest_year": {
            "year": int(warmest_year['year']),
            "anomaly": float(f"{warmest_year['anomaly']:.4f}")
        },
        "coldest_year": {
            "year": int(coldest_year['year']),
            "anomaly": float(f"{coldest_year['anomaly']:.4f}")
        }
    }
}

# Prepare decadal averages for API
decadal_data = {
    "decades": decadal_avg['decade_label'].tolist(),
    "averages": [float(f"{x:.4f}") for x in decadal_avg['anomaly'].tolist()]
}

# Save processed data
print("Saving processed data...")

# Save trends summary as JSON
with open(trends_file, 'w') as f:
    json.dump(trends_summary, f, indent=2)

# Save decadal averages as JSON
with open(decadal_file, 'w') as f:
    json.dump(decadal_data, f, indent=2)

# Save annual data as CSV for database import
df[['year', 'anomaly', 'moving_avg_5yr']].to_csv(annual_csv_file, index=False)

# Create a visualization of the temperature trend
print("Creating visualization...")
plt.figure(figsize=(12, 6))
plt.plot(df['year'], df['anomaly'], 'b-', alpha=0.5, label='Annual average')
plt.plot(df['year'], df['moving_avg_5yr'], 'r-', linewidth=2, label='5-year moving average')

# Add trend line
trend_line = slope * x + intercept
plt.plot(x, trend_line, 'g--', label=f'Trend: {trend_per_decade:.2f}°C/decade')

# Add horizontal line at zero
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly (°C)')
plt.title('Global Land-Ocean Temperature Anomalies (1880-2022)\nRelative to 1971-2000 Average')
plt.grid(True, alpha=0.3)
plt.legend()

# Save the plot
plt.savefig(plot_file, dpi=300, bbox_inches='tight')

print(f"Processing complete. Results saved to {output_dir}")
print(f"Key trends saved to {trends_file}")
print(f"Visualization saved to {plot_file}")
