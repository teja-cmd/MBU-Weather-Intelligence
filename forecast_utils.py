"""
MBU Weather Intelligence - Advanced Forecasting Functions
===========================================================
Functions for hourly, daily, and weekly forecasting with visualizations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

def create_time_features(dt_obj):
    """Create time-based features for prediction"""
    doy = dt_obj.timetuple().tm_yday
    season_map = {1:0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:3, 11:3, 12:0}
    
    return pd.DataFrame([{
        'year': dt_obj.year,
        'month': dt_obj.month,
        'day': dt_obj.day,
        'hour': dt_obj.hour,
        'day_of_year': doy,
        'day_of_week': dt_obj.weekday(),
        'week_of_year': dt_obj.isocalendar()[1],
        'quarter': (dt_obj.month - 1) // 3 + 1,
        'hour_sin': np.sin(2*np.pi*dt_obj.hour/24),
        'hour_cos': np.cos(2*np.pi*dt_obj.hour/24),
        'month_sin': np.sin(2*np.pi*dt_obj.month/12),
        'month_cos': np.cos(2*np.pi*dt_obj.month/12),
        'dow_sin': np.sin(2*np.pi*dt_obj.weekday()/7),
        'dow_cos': np.cos(2*np.pi*dt_obj.weekday()/7),
        'doy_sin': np.sin(2*np.pi*doy/365.25),
        'doy_cos': np.cos(2*np.pi*doy/365.25),
        'season': season_map[dt_obj.month],
        'is_sw_monsoon': int(dt_obj.month in [6,7,8,9]),
        'is_ne_monsoon': int(dt_obj.month in [10,11]),
        'is_summer': int(dt_obj.month in [3,4,5]),
        'is_winter': int(dt_obj.month in [12,1,2]),
        'is_daytime': int(6 <= dt_obj.hour <= 18),
        'is_peak_solar': int(10 <= dt_obj.hour <= 14),
        'is_night': int(dt_obj.hour >= 20 or dt_obj.hour <= 5),
        'is_morning': int(5 <= dt_obj.hour <= 9),
        'is_evening': int(16 <= dt_obj.hour <= 20),
        'year_trend': (dt_obj.year - 2015) / 10.0,
    }])

def predict_weather_parameter(models, scalers, features, target, dt_obj):
    """Predict a specific weather parameter"""
    X = create_time_features(dt_obj)
    X_features = X[features]
    X_scaled = scalers[target].transform(X_features)
    prediction = models[target].predict(X_scaled)[0]
    return float(prediction)

def generate_hourly_forecast(models, scalers, features, metadata, start_date):
    """Generate 24-hour forecast for a given date"""
    forecasts = []
    for hour in range(24):
        dt = datetime(start_date.year, start_date.month, start_date.day, hour)
        hourly_data = {'DateTime': dt, 'Hour': f"{hour:02d}:00"}
        
        for target in metadata.keys():
            hourly_data[target] = predict_weather_parameter(models, scalers, features, target, dt)
        
        forecasts.append(hourly_data)
    
    return pd.DataFrame(forecasts)

def generate_weekly_forecast(models, scalers, features, metadata, start_date):
    """Generate 7-day forecast starting from start_date"""
    # Use the generic n-day generator for consistency
    return generate_n_day_forecast(models, scalers, features, metadata, start_date, days=7)

def generate_n_day_forecast(models, scalers, features, metadata, start_date, days=10):
    """Generate an n-day forecast summary (daily min/max/avg) starting from start_date.

    Returns (daily_summary_df, last_day_hourly_df)
    """
    daily_forecasts = []
    last_daily_data = None

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        daily_data = generate_hourly_forecast(models, scalers, features, metadata, current_date)

        daily_summary = {'Date': current_date.strftime('%Y-%m-%d'), 'DayOfWeek': current_date.strftime('%A')}
        for target in metadata.keys():
            daily_summary[f'{target}_min'] = daily_data[target].min()
            daily_summary[f'{target}_max'] = daily_data[target].max()
            daily_summary[f'{target}_avg'] = daily_data[target].mean()

        daily_forecasts.append(daily_summary)
        last_daily_data = daily_data

    return pd.DataFrame(daily_forecasts), last_daily_data

def generate_10day_forecast(models, scalers, features, metadata, start_date):
    """Convenience wrapper to generate a 10-day forecast summary and last-day hourly data."""
    return generate_n_day_forecast(models, scalers, features, metadata, start_date, days=10)

def generate_monthly_forecast(models, scalers, features, metadata, start_date):
    """Generate 30-day forecast summary starting from start_date"""
    monthly_forecasts = []
    for day_offset in range(30):
        current_date = start_date + timedelta(days=day_offset)
        daily_data = generate_hourly_forecast(models, scalers, features, metadata, current_date)
        daily_summary = {'Date': current_date.strftime('%Y-%m-%d'), 'DayOfWeek': current_date.strftime('%A')}

        for target in metadata.keys():
            daily_summary[f'{target}_min'] = daily_data[target].min()
            daily_summary[f'{target}_max'] = daily_data[target].max()
            daily_summary[f'{target}_avg'] = daily_data[target].mean()

        monthly_forecasts.append(daily_summary)

    return pd.DataFrame(monthly_forecasts)

def create_hourly_line_plot(df_hourly, metadata, target_param, title_suffix=""):
    """Create hourly forecast line plot"""
    if target_param not in df_hourly.columns:
        return None
    
    meta = metadata.get(target_param, {})
    title = f"{meta.get('name', target_param)} - 24 Hour Forecast {title_suffix}"
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_hourly['Hour'],
        y=df_hourly[target_param],
        mode='lines+markers',
        name=target_param,
        line=dict(color='#2563eb', width=3),
        marker=dict(size=8, color='#f59e0b'),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))
    
    fig.update_layout(
        title={'text': title, 'font': {'size': 20, 'color': 'white'}, 'x': 0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        xaxis={'title': 'Time of Day', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'tickcolor': 'white'},
        yaxis={'title': f'{meta.get("unit", "")}', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'tickcolor': 'white'},
        font={'family': 'Inter', 'color': 'white', 'size': 12},
        height=400,
        margin=dict(l=50, r=20, t=80, b=50)
    )
    
    return fig

def create_multi_line_plot(df_hourly, targets, metadata):
    """Create multi-parameter line plot"""
    fig = go.Figure()
    
    colors = ['#2563eb', '#06b6d4', '#f59e0b', '#ef4444', '#10b981', '#8b5cf6']
    
    for i, target in enumerate(targets):
        if target in df_hourly.columns:
            meta = metadata.get(target, {})
            fig.add_trace(go.Scatter(
                x=df_hourly['Hour'],
                y=df_hourly[target],
                mode='lines+markers',
                name=meta.get('name', target),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6),
            ))
    
    fig.update_layout(
        title={'text': 'Multiple Parameters - 24 Hour Forecast', 'font': {'size': 20, 'color': 'white'}, 'x': 0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        xaxis={'title': 'Time of Day', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'title': 'Values', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        font={'family': 'Inter', 'color': 'white', 'size': 12},
        height=450,
        margin=dict(l=50, r=20, t=80, b=50),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.3)', bordercolor='white', borderwidth=1)
    )
    
    return fig

def create_daily_comparison_plot(df_weekly, target_param, metadata):
    """Create 7-day min/max/avg comparison"""
    meta = metadata.get(target_param, {})
    
    fig = go.Figure()
    
    # Add max line
    fig.add_trace(go.Scatter(
        x=df_weekly['Date'],
        y=df_weekly[f'{target_param}_max'],
        mode='lines+markers',
        name='Max',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=8)
    ))
    
    # Add average line
    fig.add_trace(go.Scatter(
        x=df_weekly['Date'],
        y=df_weekly[f'{target_param}_avg'],
        mode='lines+markers',
        name='Average',
        line=dict(color='#f59e0b', width=2),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(245, 158, 11, 0.2)'
    ))
    
    # Add min line
    fig.add_trace(go.Scatter(
        x=df_weekly['Date'],
        y=df_weekly[f'{target_param}_min'],
        mode='lines+markers',
        name='Min',
        line=dict(color='#06b6d4', width=2),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(6, 182, 212, 0.2)'
    ))
    
    fig.update_layout(
        title={'text': f'{meta.get("name", target_param)} - 7 Day Forecast (Min/Avg/Max)', 'font': {'size': 18, 'color': 'white'}, 'x': 0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        xaxis={'title': 'Date', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'title': f'{meta.get("unit", "")}', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        font={'family': 'Inter', 'color': 'white', 'size': 12},
        height=400,
        margin=dict(l=50, r=20, t=80, b=50),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.3)', bordercolor='white', borderwidth=1)
    )
    
    return fig

def create_heatmap_hourly(df_hourly, targets, metadata):
    """Create heatmap of hourly predictions"""
    data_matrix = []
    labels = []
    
    for target in targets:
        if target in df_hourly.columns:
            data_matrix.append(df_hourly[target].values)
            meta = metadata.get(target, {})
            labels.append(meta.get('name', target))
    
    if not data_matrix:
        return None
    
    data_matrix = np.array(data_matrix)
    
    # Normalize for heatmap
    data_normalized = (data_matrix - data_matrix.min(axis=1, keepdims=True)) / (data_matrix.max(axis=1, keepdims=True) - data_matrix.min(axis=1, keepdims=True) + 1e-8)
    
    fig = go.Figure(data=go.Heatmap(
        z=data_normalized,
        x=df_hourly['Hour'],
        y=labels,
        colorscale='Viridis',
        hovertemplate='<b>%{y}</b><br>Hour: %{x}<br>Normalized Value: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': 'Weather Parameters - Hourly Heatmap (Normalized)', 'font': {'size': 18, 'color': 'white'}, 'x': 0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'color': 'white', 'size': 12},
        height=400,
        margin=dict(l=150, r=20, t=80, b=50),
        coloraxis_colorbar=dict(tickfont=dict(color='white'), tickcolor='white')
    )
    
    return fig

def export_research_data(predictions_dict, model_results, metadata, start_date):
    """Export research paper data with statistics and metrics"""
    export_data = {
        'Export_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Forecast_Date': start_date.strftime('%Y-%m-%d'),
        'Institution': 'Mohan Babu University, Tirupati',
        'Data_Source': 'NASA POWER Dataset'
    }
    
    # Model performance metrics
    export_data['Model_Metrics'] = {}
    for target, metrics in model_results.items():
        export_data['Model_Metrics'][target] = {
            'R2_Score': metrics['R2'],
            'MAE': metrics['MAE'],
            'RMSE': metrics['RMSE']
        }
    
    # Average performance
    avg_r2 = np.mean([m['R2'] for m in model_results.values()])
    avg_mae = np.mean([m['MAE'] for m in model_results.values()])
    avg_rmse = np.mean([m['RMSE'] for m in model_results.values()])
    
    export_data['Overall_Performance'] = {
        'Avg_R2': float(avg_r2),
        'Avg_MAE': float(avg_mae),
        'Avg_RMSE': float(avg_rmse),
        'Models_Count': len(model_results)
    }
    
    # Forecast predictions
    export_data['Forecast_Data'] = predictions_dict
    
    return export_data

def generate_research_report(export_data, metadata):
    """Generate research paper formatted report"""
    report = """
# MBU Weather Intelligence System - Research Report
## Mohan Babu University, Tirupati

### I. Executive Summary
This report documents the AI-powered weather prediction system developed for Mohan Babu University,
utilizing advanced machine learning models trained on NASA POWER satellite data (2015-present).

### II. Methodology
**Data Source:** NASA POWER - Prediction Of Worldwide Energy Resources
**Location:** Tirupati, India (13.1939°N, 79.8941°E)
**Training Period:** 2015-present (~10 years of hourly data)
**Models:** XGBoost Regressors & Random Forest Classifiers
**Time Features:** 26 engineered temporal and cyclical features
**Train/Test Split:** 80/20 (temporal, non-shuffled)

### III. Model Performance
"""
    
    # Add model metrics
    report += f"\nAverage R² Score: {export_data['Overall_Performance']['Avg_R2']:.4f}\n"
    report += f"Average MAE: {export_data['Overall_Performance']['Avg_MAE']:.4f}\n"
    report += f"Average RMSE: {export_data['Overall_Performance']['Avg_RMSE']:.4f}\n"
    report += f"Total Models Trained: {export_data['Overall_Performance']['Models_Count']}\n"
    
    report += "\n### IV. Predictions\nGenerated on: " + export_data['Export_Date'] + "\n"
    report += f"Forecast Date: {export_data['Forecast_Date']}\n"
    
    return report
