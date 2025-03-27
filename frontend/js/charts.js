// Chart creation and configuration for Climate Data Visualization

// Global chart instances
let temperatureChart;
let decadalChart;
let customRangeChart;

// Create the main temperature chart
function createTemperatureChart(data) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    
    // Prepare data
    const years = data.map(item => item.year);
    const anomalies = data.map(item => item.anomaly);
    const movingAvg = data.map(item => item.moving_avg_5yr);
    
    // Calculate trend line (simple linear regression)
    const trendLine = calculateTrendLine(years, anomalies);
    
    temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Annual Temperature Anomaly',
                    data: anomalies,
                    backgroundColor: CONFIG.COLORS.ANNUAL,
                    borderColor: CONFIG.COLORS.ANNUAL_BORDER,
                    borderWidth: 1,
                    pointRadius: 2,
                    pointHoverRadius: 5,
                    fill: false
                },
                {
                    label: '5-Year Moving Average',
                    data: movingAvg,
                    backgroundColor: 'transparent',
                    borderColor: CONFIG.COLORS.MOVING_AVG,
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    fill: false
                },
                {
                    label: 'Trend Line',
                    data: trendLine,
                    backgroundColor: 'transparent',
                    borderColor: CONFIG.COLORS.TREND_LINE,
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    },
                    ticks: {
                        maxTicksLimit: 20
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature Anomaly (°C)'
                    },
                    grid: {
                        color: (context) => {
                            if (context.tick.value === 0) {
                                return CONFIG.COLORS.ZERO_LINE;
                            }
                            return 'rgba(0, 0, 0, 0.1)';
                        },
                        lineWidth: (context) => {
                            if (context.tick.value === 0) {
                                return 2;
                            }
                            return 1;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Global Temperature Anomalies (1880-2022)',
                    font: {
                        size: 16
                    }
                },
                subtitle: {
                    display: true,
                    text: 'Relative to 1971-2000 Average',
                    font: {
                        size: 14,
                        style: 'italic'
                    },
                    padding: {
                        bottom: 10
                    }
                }
            }
        }
    });
}

// Create the decadal averages chart
function createDecadalChart(data) {
    const ctx = document.getElementById('decadalChart').getContext('2d');
    
    decadalChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.decades,
            datasets: [{
                label: 'Decadal Average Temperature Anomaly',
                data: data.averages,
                backgroundColor: CONFIG.COLORS.DECADAL,
                borderColor: CONFIG.COLORS.DECADAL_BORDER,
                borderWidth: 1
            }]
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Decade'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature Anomaly (°C)'
                    },
                    grid: {
                        color: (context) => {
                            if (context.tick.value === 0) {
                                return CONFIG.COLORS.ZERO_LINE;
                            }
                            return 'rgba(0, 0, 0, 0.1)';
                        },
                        lineWidth: (context) => {
                            if (context.tick.value === 0) {
                                return 2;
                            }
                            return 1;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Decadal Average Temperature Anomalies',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Create the custom range chart
function createCustomRangeChart(data, startYear, endYear) {
    const ctx = document.getElementById('customRangeChart').getContext('2d');
    
    // Filter data for selected range
    const filteredData = data.filter(item => item.year >= startYear && item.year <= endYear);
    
    // Prepare data
    const years = filteredData.map(item => item.year);
    const anomalies = filteredData.map(item => item.anomaly);
    
    // Destroy previous chart if it exists
    if (customRangeChart) {
        customRangeChart.destroy();
    }
    
    customRangeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: 'Temperature Anomaly',
                data: anomalies,
                backgroundColor: CONFIG.COLORS.CUSTOM_RANGE,
                borderColor: CONFIG.COLORS.CUSTOM_RANGE_BORDER,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 6,
                fill: false
            }]
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature Anomaly (°C)'
                    },
                    grid: {
                        color: (context) => {
                            if (context.tick.value === 0) {
                                return CONFIG.COLORS.ZERO_LINE;
                            }
                            return 'rgba(0, 0, 0, 0.1)';
                        },
                        lineWidth: (context) => {
                            if (context.tick.value === 0) {
                                return 2;
                            }
                            return 1;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Temperature Anomalies (${startYear}-${endYear})`,
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Helper function to calculate trend line
function calculateTrendLine(years, anomalies) {
    // Simple linear regression
    const n = years.length;
    
    // Calculate means
    const meanX = years.reduce((sum, x) => sum + x, 0) / n;
    const meanY = anomalies.reduce((sum, y) => sum + y, 0) / n;
    
    // Calculate slope and intercept
    let numerator = 0;
    let denominator = 0;
    
    for (let i = 0; i < n; i++) {
        numerator += (years[i] - meanX) * (anomalies[i] - meanY);
        denominator += (years[i] - meanX) ** 2;
    }
    
    const slope = numerator / denominator;
    const intercept = meanY - slope * meanX;
    
    // Generate trend line points
    return years.map(year => slope * year + intercept);
}
