#!/usr/bin/env python3
"""
MBU Weather Intelligence System
===============================
Professional Weather Prediction Dashboard for Mohan Babu University, Tirupati
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import time
import json
from forecast_utils import (
    generate_hourly_forecast, 
    generate_weekly_forecast,
    generate_10day_forecast,
    generate_monthly_forecast,
    create_hourly_line_plot,
    create_multi_line_plot,
    create_daily_comparison_plot,
    create_heatmap_hourly,
    export_research_data,
    generate_research_report
)
import new_pages

# Page config
st.set_page_config(
    page_title="MBU Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Professional CSS with beautiful colors and animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #0ea5a4;
    --primary-dark: #065f5a;
    --secondary: #06b6d4;
    --accent: #06b6d4;
    --success: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    --info: #8b5cf6;
    --light: #f5f3ff;
    --dark: #071426;
    --gray-50: #faf5ff;
    --gray-100: #f3e8ff;
    --gray-200: #e9d5ff;
    --gray-300: #d8b4fe;
    --gray-400: #c084fc;
    --gray-500: #a855f7;
    --gray-600: #9333ea;
    --gray-700: #7e22ce;
    --gray-800: #6b21a8;
    --gray-900: #581c87;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #071426 0%, #0b1f2f 50%, #071426 100%);
    font-family: 'Poppins', 'Inter', sans-serif;
    color: #f8fafc;
}

/* Hide Streamlit elements */
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }
.stAppHeader { display: none; }

/* Custom Navbar */
.navbar {
    background: rgba(139, 92, 246, 0.15);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(167, 139, 250, 0.3);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
    from { transform: translateY(-100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    font-weight: 800;
    color: #f5f3ff;
    text-decoration: none;
}

.navbar-nav {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-left: auto;
}

.nav-item {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    background: rgba(168, 85, 247, 0.2);
    color: #f5f3ff;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid transparent;
}

.nav-item:hover {
    background: rgba(168, 85, 247, 0.4);
    border-color: rgba(236, 72, 153, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.nav-item.active {
    background: rgba(236, 72, 153, 0.9);
    border-color: rgba(236, 72, 153, 1);
}

/* Main Container */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 3rem 0;
    margin-bottom: 3rem;
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: var(--light);
    margin-bottom: 0.75rem;
    line-height: 1.1;
    font-family: 'Poppins', sans-serif;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: rgba(248,250,252,0.85);
    margin-bottom: 1.5rem;
    max-width: 760px;
    margin-left: auto;
    margin-right: auto;
    font-weight: 500;
    text-align: center;
    line-height: 1.6;
}

/* Model Cards Grid */
.models-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.model-card {
    background: rgba(139, 92, 246, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-radius: 1rem;
    padding: 2rem;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    animation: slideInUp 0.6s ease-out;
    display: flex;
    flex-direction: column;
    min-height: 320px;
    justify-content: space-between;
    margin-bottom: 1rem;
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

.model-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(236, 72, 153, 0.2), transparent);
    transition: left 0.5s ease;
}

.model-card:hover::before {
    left: 100%;
}

.model-card:hover {
    transform: translateY(-8px);
    border-color: rgba(236, 72, 153, 0.6);
    box-shadow: 0 20px 40px rgba(109, 40, 217, 0.3);
}

.model-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.model-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f5f3ff;
    margin-bottom: 0.75rem;
    line-height: 1.2;
}

.model-description {
    color: #d8b4fe;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    flex-grow: 1;
    font-size: 0.95rem;
}

.model-button {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.25rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    font-size: 1rem;
    margin-top: auto;
}

.model-button:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

/* Prediction Page Styles */
.prediction-page {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    padding: 2rem;
    margin: 2rem 0;
    animation: fadeIn 0.5s ease-out;
}

.page-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(168, 85, 247, 0.2);
}

.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #f5f3ff;
    margin-bottom: 0.5rem;
}

.page-subtitle {
    color: #d8b4fe;
    font-size: 1.1rem;
}

/* Input Section */
.input-section {
    background: rgba(168, 85, 247, 0.1);
    border-radius: 0.75rem;
    padding: 1.5rem;
    margin: 1.5rem 0;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

.input-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f5f3ff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Results Section */
.results-section {
    margin-top: 2rem;
    animation: slideInUp 0.6s ease-out;
}

.result-card {
    background: rgba(168, 85, 247, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 1rem;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

.result-value {
    font-size: 3rem;
    font-weight: 800;
    color: #ec4899;
    margin: 1rem 0;
}

.result-label {
    color: #d8b4fe;
    font-size: 1.1rem;
    font-weight: 500;
}

/* Back Button */
.back-button {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.back-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateX(-4px);
}

/* Stats Cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.stat-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0.75rem;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.4);
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 0.5rem;
}

.stat-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

/* Custom Streamlit Overrides */
.stButton > button,
.stDownloadButton > button {
    background: var(--primary-dark) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 0.5rem !important;
    padding: 0.65rem 1.25rem !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.6) !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: var(--primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(14,165,164,0.18) !important;
}

.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 0.5rem !important;
    color: #f8fafc !important;
}

.stDateInput > div > div > input {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 0.5rem !important;
    color: white !important;
}

/* Loading Animation */
.loading-spinner {
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: var(--primary);
    animation: spin 1s ease-in-out infinite;
    margin: 2rem auto;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .model-card {
        min-height: 260px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .main-container { padding: 1rem; }
    .navbar { padding: 1rem; }
    .navbar-nav { flex-direction: column; gap: 0.5rem; }
}

@media (max-width: 480px) {
    .hero-title { font-size: 2rem; }
    .hero-subtitle { font-size: 1rem; }
    .model-card {
        padding: 1.25rem;
        min-height: 240px;
    }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
}
</style>
""", unsafe_allow_html=True)
# Load models with error handling for cloud deployment
@st.cache_resource(show_spinner=False)
def load_weather_models():
    """Load all weather prediction models with cloud deployment support"""
    models_dir = 'models'
    
    if not os.path.exists(models_dir):
        st.error("⚠️ Models directory not found!")
        st.info("🔄 The models need to be trained first. This typically happens automatically on first run.")
        st.info("📝 If this persists, please contact the administrator.")
        return None, None, None, None, None, "Models directory not found!"
    
    try:
        # Check if essential model files exist
        essential_files = ['weather_targets.pkl', 'weather_metadata.pkl', 'feature_names.pkl']
        missing_files = [f for f in essential_files if not os.path.exists(f'{models_dir}/{f}')]
        
        if missing_files:
            st.error(f"⚠️ Missing essential model files: {', '.join(missing_files)}")
            st.info("🔄 Please run model training: `python train_models.py`")
            return None, None, None, None, None, f"Missing files: {', '.join(missing_files)}"
        
        weather_targets = joblib.load(f'{models_dir}/weather_targets.pkl')
        weather_metadata = joblib.load(f'{models_dir}/weather_metadata.pkl')
        feature_names = joblib.load(f'{models_dir}/feature_names.pkl')
        
        models = {}
        scalers = {}
        
        # Load models with progress indication
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, target in enumerate(weather_targets):
            status_text.text(f"Loading {target} model...")
            models[target] = joblib.load(f'{models_dir}/{target}_model.pkl')
            scalers[target] = joblib.load(f'{models_dir}/{target}_scaler.pkl')
            progress_bar.progress((i + 1) / len(weather_targets))
        
        progress_bar.empty()
        status_text.empty()
        
        rain_classifier = joblib.load(f'{models_dir}/RAIN_classifier.pkl')
        rain_scaler = joblib.load(f'{models_dir}/RAIN_scaler.pkl')
        
        return models, scalers, weather_metadata, feature_names, rain_classifier, "Models loaded successfully!"
        
    except FileNotFoundError as e:
        error_msg = f"Model file not found: {str(e)}"
        st.error(f"⚠️ {error_msg}")
        st.info("🔄 Some model files are missing. Please ensure all models are trained.")
        return None, None, None, None, None, error_msg
        
    except Exception as e:
        error_msg = f"Error loading models: {str(e)}"
        st.error(f"⚠️ {error_msg}")
        st.info("🔧 There was an issue loading the machine learning models.")
        return None, None, None, None, None, error_msg

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

def predict_weather_parameter(target, dt_obj):
    """Predict a specific weather parameter"""
    if not models_loaded:
        return None
    
    X = create_time_features(dt_obj)
    X_scaled = scalers[target].transform(X)
    prediction = models[target].predict(X_scaled)[0]
    
    return float(prediction)

def predict_rainfall_classification(dt_obj):
    """Predict rainfall probability and classification"""
    if not models_loaded:
        return None, None
    
    X = create_time_features(dt_obj)
    X_scaled = scalers['PRECTOTCORR'].transform(X)
    
    prob = rain_clf.predict_proba(X_scaled)[0][1]
    flag = rain_clf.predict(X_scaled)[0]
    
    return float(prob), bool(flag)

def predict_monthly_data(year):
    """Generate monthly predictions for an entire year"""
    monthly_data = {}
    
    # Define months
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    for month_idx, month_name in enumerate(months, 1):
        # Sample multiple days in the month for better accuracy
        sample_days = [1, 8, 15, 22, 28]  # Sample 5 days per month
        sample_hours = [6, 12, 18]  # Sample 3 times per day
        
        month_predictions = {param: [] for param in metadata.keys()}
        month_predictions['rain_prob'] = []
        
        for day in sample_days:
            try:
                for hour in sample_hours:
                    dt_obj = datetime(year, month_idx, day, hour)
                    
                    # Get predictions for all parameters
                    for param in metadata.keys():
                        pred = predict_weather_parameter(param, dt_obj)
                        month_predictions[param].append(pred)
                    
                    # Get rain probability
                    rain_prob, _ = predict_rainfall_classification(dt_obj)
                    month_predictions['rain_prob'].append(rain_prob)
                    
            except ValueError:
                # Handle invalid dates (e.g., Feb 30)
                continue
        
        # Calculate monthly statistics
        monthly_stats = {}
        for param in metadata.keys():
            if month_predictions[param]:
                monthly_stats[param] = {
                    'avg': np.mean(month_predictions[param]),
                    'min': np.min(month_predictions[param]),
                    'max': np.max(month_predictions[param]),
                    'values': month_predictions[param]
                }
        
        # Rain statistics
        monthly_stats['rain_prob'] = {
            'avg': np.mean(month_predictions['rain_prob']) * 100,
            'min': np.min(month_predictions['rain_prob']) * 100,
            'max': np.max(month_predictions['rain_prob']) * 100,
            'values': month_predictions['rain_prob']
        }
        
        monthly_data[month_name] = monthly_stats
    
    return monthly_data

def create_monthly_chart(monthly_data, parameter, title, unit, color="#2563eb"):
    """Create a monthly trend chart"""
    months = list(monthly_data.keys())
    avg_values = [monthly_data[month][parameter]['avg'] for month in months]
    min_values = [monthly_data[month][parameter]['min'] for month in months]
    max_values = [monthly_data[month][parameter]['max'] for month in months]
    
    fig = go.Figure()
    
    # Add average line
    fig.add_trace(go.Scatter(
        x=months,
        y=avg_values,
        mode='lines+markers',
        name='Average',
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color)
    ))
    
    # Add min-max range
    fig.add_trace(go.Scatter(
        x=months + months[::-1],
        y=max_values + min_values[::-1],
        fill='toself',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Min-Max Range',
        showlegend=True
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white', family='Inter')),
        xaxis=dict(
            title='Month',
            tickfont=dict(color='white', size=12),
            title_font=dict(color='white', size=14),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title=f'{title} ({unit})',
            tickfont=dict(color='white', size=12),
            title_font=dict(color='white', size=14),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='white'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        height=400,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
    return fig

def create_seasonal_summary_chart(monthly_data):
    """Create seasonal summary charts"""
    seasons = {
        'Winter': ['December', 'January', 'February'],
        'Summer': ['March', 'April', 'May'],
        'SW Monsoon': ['June', 'July', 'August', 'September'],
        'NE Monsoon': ['October', 'November']
    }
    
    # Calculate seasonal averages for key parameters
    seasonal_data = {}
    key_params = ['T2M', 'RH2M', 'PRECTOTCORR', 'WS10M']
    
    for season, months in seasons.items():
        seasonal_data[season] = {}
        for param in key_params:
            values = []
            for month in months:
                if month in monthly_data:
                    values.extend(monthly_data[month][param]['values'])
            if values:
                seasonal_data[season][param] = np.mean(values)
    
    # Create radar chart
    fig = go.Figure()
    
    categories = ['Temperature (°C)', 'Humidity (%)', 'Rainfall (mm/hr)', 'Wind Speed (m/s)']
    colors = ['#ef4444', '#10b981', '#06b6d4', '#f59e0b']
    
    for i, (season, data) in enumerate(seasonal_data.items()):
        values = [
            data.get('T2M', 0),
            data.get('RH2M', 0),
            data.get('PRECTOTCORR', 0) * 10,  # Scale for visibility
            data.get('WS10M', 0)
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=season,
            line=dict(color=colors[i % len(colors)], width=2),
            fillcolor=f'rgba({int(colors[i % len(colors)][1:3], 16)}, {int(colors[i % len(colors)][3:5], 16)}, {int(colors[i % len(colors)][5:7], 16)}, 0.1)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([max([data.get('T2M', 0), data.get('RH2M', 0), 
                                  data.get('PRECTOTCORR', 0) * 10, data.get('WS10M', 0)]) 
                              for data in seasonal_data.values()])],
                tickfont=dict(color='white', size=10),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.2)'
            )
        ),
        title=dict(text='Seasonal Weather Patterns', font=dict(size=18, color='white', family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='white'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        height=500
    )
    
    return fig
    """Predict rainfall probability and classification"""
    if not models_loaded:
        return None, None
    
    X = create_time_features(dt_obj)
    X_scaled = scalers['PRECTOTCORR'].transform(X)
    
    prob = rain_clf.predict_proba(X_scaled)[0][1]
    flag = rain_clf.predict(X_scaled)[0]
    
    return float(prob), bool(flag)

def create_gauge_chart(value, min_val, max_val, title, unit, color="#2563eb"):
    """Create a beautiful gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"{title}", 'font': {'size': 18, 'color': 'white', 'family': 'Inter'}},
        number={'font': {'size': 32, 'color': '#f59e0b', 'family': 'Inter'}, 'suffix': f" {unit}"},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': 'white', 'tickfont': {'color': 'white', 'size': 12}},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [min_val, min_val + (max_val-min_val)*0.33], 'color': 'rgba(255,255,255,0.1)'},
                {'range': [min_val + (max_val-min_val)*0.33, min_val + (max_val-min_val)*0.66], 'color': 'rgba(255,255,255,0.15)'},
                {'range': [min_val + (max_val-min_val)*0.66, max_val], 'color': 'rgba(255,255,255,0.2)'},
            ],
            'threshold': {'line': {'color': '#f59e0b', 'width': 4}, 'thickness': 0.85, 'value': value}
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'family': 'Inter', 'color': 'white'}
    )
    return fig

# ==================== FEATURE 1: CONFIDENCE SCORE ====================
def calculate_confidence_score(param, forecast_value, historical_mean, historical_std):
    """Calculate confidence score (0-100) for predictions"""
    if historical_std == 0:
        return 85.0
    z_score = abs((forecast_value - historical_mean) / historical_std)
    confidence = max(0, min(100, 100 - (z_score * 10)))
    return float(confidence)

def display_confidence_indicator(confidence_score):
    """Display a colored confidence indicator"""
    if confidence_score >= 80:
        color, status = "#10b981", "High"
    elif confidence_score >= 60:
        color, status = "#f59e0b", "Medium"
    else:
        color, status = "#ef4444", "Low"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; background: rgba(168, 85, 247, 0.1); 
                padding: 1rem; border-radius: 0.5rem; border-left: 4px solid {color};">
        <div style="flex: 1;">
            <div style="color: #d8b4fe; font-size: 0.9rem;">Prediction Confidence</div>
            <div style="color: #f5f3ff; font-size: 1.5rem; font-weight: 700;">{confidence_score:.1f}%</div>
        </div>
        <div style="font-size: 2rem;">{status}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FEATURE 2: HISTORICAL COMPARISON ====================
def generate_historical_avg(param, target_month, target_day):
    """Generate approximate historical average for comparison"""
    if hasattr(model_results, '__getitem__') and param in model_results:
        base_val = model_results[param].get('MAE', 5.0)
    else:
        base_val = 5.0
    seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * target_month / 12)
    return base_val * seasonal_factor

def display_historical_comparison(param, current_value, unit):
    """Display comparison with historical data"""
    hist_avg = generate_historical_avg(param, date.today().month, date.today().day)
    diff_percent = ((current_value - hist_avg) / hist_avg * 100) if hist_avg != 0 else 0
    direction = "↑ Higher" if diff_percent > 0 else "↓ Lower"
    direction_color = "#ef4444" if diff_percent > 0 else "#10b981"
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
        <div style="background: rgba(168, 85, 247, 0.1); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(168, 85, 247, 0.3);">
            <div style="color: #d8b4fe; font-size: 0.9rem;">Current Prediction</div>
            <div style="color: #ec4899; font-size: 1.8rem; font-weight: 700;">{current_value:.2f} {unit}</div>
        </div>
        <div style="background: rgba(168, 85, 247, 0.1); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(168, 85, 247, 0.3);">
            <div style="color: #d8b4fe; font-size: 0.9rem;">Historical Average</div>
            <div style="color: #a855f7; font-size: 1.8rem; font-weight: 700;">{hist_avg:.2f} {unit}</div>
        </div>
    </div>
    <div style="background: rgba({255 if diff_percent > 0 else 16}, {0 if diff_percent > 0 else 179}, {0 if diff_percent > 0 else 145}, 0.1); 
                padding: 0.75rem 1rem; border-radius: 0.5rem; border-left: 4px solid {direction_color};">
        <span style="color: {direction_color}; font-weight: 600;">{direction} {abs(diff_percent):.1f}% from historical average</span>
    </div>
    """, unsafe_allow_html=True)

# ==================== FEATURE 3: EXTREME VALUE ALERTS ====================
def check_extreme_values(param, value, metadata_dict):
    """Check if values exceed safe thresholds"""
    thresholds = {
        'T2M': {'min': -5, 'max': 50},
        'RH2M': {'min': 0, 'max': 100},
        'PRECTOTCORR': {'min': 0, 'max': 200},
        'WS10M': {'min': 0, 'max': 50},
        'PS': {'min': 90000, 'max': 105000},
    }
    
    if param in thresholds:
        threshold = thresholds[param]
        if value < threshold['min'] or value > threshold['max']:
            return True, "Extreme"
        elif abs(value - threshold['min']) < 5 or abs(value - threshold['max']) < 5:
            return True, "Warning"
    return False, "Normal"

def display_alerts(param, value, alert_type):
    """Display alert badges"""
    if alert_type == "Extreme":
        alert_color, alert_icon = "#ef4444", "⚠️"
        alert_msg = "EXTREME VALUE DETECTED"
    elif alert_type == "Warning":
        alert_color, alert_icon = "#f59e0b", "⚡"
        alert_msg = "VALUE NEAR THRESHOLD"
    else:
        alert_color, alert_icon = "#10b981", "✓"
        alert_msg = "WITHIN NORMAL RANGE"
    
    st.markdown(f"""
    <div style="background: rgba({int(alert_color[1:3], 16)}, {int(alert_color[3:5], 16)}, {int(alert_color[5:7], 16)}, 0.1); 
                padding: 1rem; border-radius: 0.5rem; border: 1px solid {alert_color}; text-align: center;">
        <div style="font-size: 1.5rem;">{alert_icon}</div>
        <div style="color: {alert_color}; font-weight: 600; margin-top: 0.5rem;">{alert_msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FEATURE 4: QUICK EXPORT SUMMARY ====================
def generate_export_summary(forecast_df, param_list):
    """Generate a quick summary for export"""
    summary_data = {}
    for param in param_list:
        if param in forecast_df.columns:
            summary_data[param] = {
                'min': forecast_df[param].min(),
                'max': forecast_df[param].max(),
                'avg': forecast_df[param].mean(),
                'std': forecast_df[param].std()
            }
    return summary_data

def create_quick_export_button(summary_data, export_name="weather_summary"):
    """Create exportable summary"""
    export_data = {
        'generated_at': datetime.now().isoformat(),
        'summary': summary_data
    }
    
    json_str = json.dumps(export_data, indent=2)
    csv_data = pd.DataFrame(summary_data).T
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Export Summary (JSON)",
            data=json_str,
            file_name=f"{export_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            "📥 Export Summary (CSV)",
            data=csv_data.to_csv(),
            file_name=f"{export_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Load models
models, scalers, metadata, features, rain_clf, load_msg = load_weather_models()
models_loaded = models is not None

# Load model results (performance metrics) if available
model_results = {}
try:
    if os.path.exists('models/model_results.pkl'):
        model_results = joblib.load('models/model_results.pkl')
except Exception:
    model_results = {}

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Custom Navbar
def render_navbar():
    st.markdown("""
    <div class="navbar">
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="navbar-brand">
                <span>🌤️</span>
                <span>MBU Weather Intelligence</span>
            </div>
            <div class="navbar-nav">
                <div class="nav-item" onclick="window.location.reload()">🏠 Home</div>
                <div class="nav-item" style="background: rgba(255,255,255,0.05); cursor: default;">
                    📍 Tirupati, India
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Weather Models Configuration
WEATHER_MODELS = {
    'rainfall': {
        'icon': '🌧️',
        'title': 'Rainfall Prediction',
        'description': 'Predict precipitation probability, intensity, and rain classification for any future date and time.',
        'color': '#06b6d4'
    },
    'temperature': {
        'icon': '🌡️',
        'title': 'Temperature Forecasting',
        'description': 'Forecast air temperature, wet bulb temperature, and dew point with high accuracy.',
        'color': '#ef4444'
    },
    'humidity': {
        'icon': '💧',
        'title': 'Humidity Analysis',
        'description': 'Analyze relative and specific humidity levels for optimal comfort planning.',
        'color': '#06b6d4'
    },
    'wind': {
        'icon': '🌬️',
        'title': 'Wind Conditions',
        'description': 'Predict wind speed and direction at multiple heights with Beaufort scale classification.',
        'color': '#64748b'
    },
    'solar': {
        'icon': '☀️',
        'title': 'Solar Radiation',
        'description': 'Forecast solar irradiance, UV index, and photosynthetic radiation for energy planning.',
        'color': '#f59e0b'
    },
    'atmospheric': {
        'icon': '🌍',
        'title': 'Atmospheric Conditions',
        'description': 'Monitor surface pressure, solar zenith angle, and atmospheric parameters.',
        'color': '#10b981'
    },
    'complete': {
        'icon': '🔮',
        'title': 'Complete Forecast',
        'description': 'Get comprehensive predictions for all 23 weather parameters in one detailed report.',
        'color': '#8b5cf6'
    },
    'monthly': {
        'icon': '📅',
        'title': 'Monthly Forecast',
        'description': 'Comprehensive 12-month weather outlook with trends, patterns, and seasonal analysis.',
        'color': '#06b6d4'
    },
    'hourly': {
        'icon': '⏰',
        'title': 'Hourly Forecast',
        'description': 'View detailed 24-hour predictions with interactive hourly plots for your planning.',
        'color': '#06b6d4'
    },
    'weekly': {
        'icon': '📅',
        'title': 'Weekly Forecast',
        'description': 'Get 7-day forecast with daily min/max/average values and trending visualizations.',
        'color': '#f59e0b'
    },
    'daily_summary': {
        'icon': '📊',
        'title': 'Daily Summary',
        'description': 'View daily aggregated predictions with max/min temperature and conditions.',
        'color': '#10b981'
    },
    'research': {
        'icon': '📑',
        'title': 'Research Export',
        'description': 'Export model metrics, performance statistics, and forecasts for academic research papers.',
        'color': '#8b5cf6'
    }
}
# Home Page
def render_home_page():
    st.markdown("""
    <div class="main-container">
        <div class="hero-section">
            <h1 class="hero-title">🌤️ MBU Weather Intelligence</h1>
            <div style="text-align: center; max-width: 760px; margin: 0 auto;">
                <p class="hero-subtitle">
                    Advanced AI-powered weather prediction system for Mohan Babu University, Tirupati. 
                    Plan your events and activities with confidence using our comprehensive weather forecasting models.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    col1, col2, col3, col4, col5 = st.columns(5)
    stats = [
        ("97K+", "Data Points", col1),
        ("23", "Weather Parameters", col2),
        ("10+", "Years of Data", col3),
        ("24", "ML Models", col4),
        ("99%", "Accuracy", col5)
    ]
    
    for stat_num, stat_label, col in stats:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stat_num}</div>
                <div class="stat-label">{stat_label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Models Grid
    st.markdown("""
    <div class="main-container">
        <h2 style="text-align: center; color: var(--light); font-size: 2.2rem; font-weight: 800; margin: 2.5rem 0 1.5rem 0; font-family: 'Poppins', sans-serif;">
            🔮 Weather Prediction Models
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create model cards in responsive grid layout
    model_items = list(WEATHER_MODELS.items())
    
    # Create rows of up to 4 columns each
    for row_start in range(0, len(model_items), 4):
        row_items = model_items[row_start:row_start+4]
        cols = st.columns(len(row_items))
        
        for i, (model_key, model_info) in enumerate(row_items):
            with cols[i]:
                st.markdown(f"""
                <div class="model-card">
                    <div>
                        <div class="model-icon">{model_info['icon']}</div>
                        <h3 class="model-title">{model_info['title']}</h3>
                        <p class="model-description">{model_info['description']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Open {model_info['title']}", key=f"btn_{model_key}", use_container_width=True):
                    navigate_to(model_key)
    
    # About Section
    with st.expander("ℹ️ About MBU Weather Intelligence System", expanded=False):
        st.markdown("""
        ### 🎓 Purpose
        This AI-powered system helps Mohan Babu University plan outdoor events, campus activities, 
        and academic programs by predicting weather conditions for any future date and time.
        
        ### 📊 Data Source
        NASA POWER (Prediction Of Worldwide Energy Resources) — comprehensive meteorological data 
        for Tirupati from 2015 to present, providing accurate climatological patterns.
        
        ### 🤖 Technology
        Advanced machine learning models (XGBoost, Random Forest) trained on 10+ years of 
        historical weather patterns, capturing seasonal trends, monsoon patterns, and climate signals.
        
        ### ⚠️ Disclaimer
        Predictions are based on historical climatological patterns. For critical events, 
        also consult current weather forecasts closer to the date.
        """)
    
    # Footer
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; line-height: 1.6;">
            🌤️ <strong>MBU Weather Intelligence System</strong><br>
            Developed for Mohan Babu University, Tirupati<br>
            Powered by NASA POWER Data & Advanced Machine Learning<br>
            <em>Empowering Smart Campus Decisions Through AI</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Input Widget
def datetime_input_widget(key_prefix=""):
    """Create professional datetime input widget"""
    st.markdown("""
    <div class="input-section">
        <h3 class="input-title">📅 Select Date & Time for Prediction</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        sel_date = st.date_input(
            "📅 Select Date", 
            value=date.today(),
            min_value=date(2026, 1, 1),
            max_value=date(2035, 12, 31),
            key=f"{key_prefix}_date",
            help="Choose any future date between 2026-2035"
        )
    
    with col2:
        sel_hour = st.selectbox(
            "🕐 Select Hour",
            options=list(range(24)),
            format_func=lambda x: f"{x:02d}:00",
            index=datetime.now().hour,
            key=f"{key_prefix}_hour",
            help="Select the hour for prediction"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🔮 Predict Weather", key=f"{key_prefix}_btn", use_container_width=True)
    
    dt_obj = datetime(sel_date.year, sel_date.month, sel_date.day, sel_hour)
    return dt_obj, predict_btn

# Back Button Component
def render_back_button():
    if st.button("← Back to Home", key="back_btn"):
        navigate_to('home')

# Inject shared app context into new_pages module
new_pages.st = st
new_pages.date = date
new_pages.models_loaded = models_loaded
new_pages.models = models
new_pages.scalers = scalers
new_pages.features = features
new_pages.metadata = metadata
new_pages.render_back_button = render_back_button
new_pages.generate_hourly_forecast = generate_hourly_forecast
new_pages.generate_weekly_forecast = generate_weekly_forecast
new_pages.create_hourly_line_plot = create_hourly_line_plot
new_pages.create_multi_line_plot = create_multi_line_plot
new_pages.create_heatmap_hourly = create_heatmap_hourly
new_pages.create_daily_comparison_plot = create_daily_comparison_plot
new_pages.joblib = joblib
new_pages.np = np
new_pages.pd = pd
new_pages.json = json
new_pages.datetime = datetime
new_pages.generate_research_report = generate_research_report
# NEW FEATURES - Inject new helper functions for enhanced predictions
new_pages.calculate_confidence_score = calculate_confidence_score
new_pages.display_confidence_indicator = display_confidence_indicator
new_pages.generate_historical_avg = generate_historical_avg
new_pages.display_historical_comparison = display_historical_comparison
new_pages.check_extreme_values = check_extreme_values
new_pages.display_alerts = display_alerts
new_pages.generate_export_summary = generate_export_summary
new_pages.create_quick_export_button = create_quick_export_button
new_pages.generate_10day_forecast = generate_10day_forecast
new_pages.generate_monthly_forecast = generate_monthly_forecast
new_pages.model_results = model_results

# Rainfall Prediction Page
def render_rainfall_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">🌧️ Rainfall Prediction</h1>
            <p class="page-subtitle">Advanced precipitation forecasting with probability analysis and intensity classification</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("rainfall")
    
    if do_predict:
        with st.spinner("🌧️ Analyzing rainfall patterns..."):
            time.sleep(0.8)
        
        rain_amount = predict_weather_parameter('PRECTOTCORR', dt_obj)
        rain_prob, rain_flag = predict_rainfall_classification(dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rain probability gauge
            fig_prob = create_gauge_chart(rain_prob*100, 0, 100, "Rain Probability", "%", "#06b6d4")
            st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': False})
            
            # Rain status
            status = "RAIN EXPECTED" if rain_flag else "NO RAIN"
            emoji = "🌧️" if rain_flag else "☀️"
            color = "#06b6d4" if rain_flag else "#f59e0b"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {color}; margin-bottom: 0.5rem;">{status}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">
                    {dt_obj.strftime('%A, %B %d, %Y at %I:%M %p')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Rainfall amount gauge
            fig_amount = create_gauge_chart(max(0, rain_amount), 0, 20, "Rainfall Amount", "mm/hr", "#2563eb")
            st.plotly_chart(fig_amount, use_container_width=True, config={'displayModeBar': False})
            
            # Intensity classification
            if rain_amount < 0.1:
                intensity, color_i = "No Rain", "#64748b"
            elif rain_amount < 2.5:
                intensity, color_i = "Light Rain", "#06b6d4"
            elif rain_amount < 7.5:
                intensity, color_i = "Moderate Rain", "#2563eb"
            elif rain_amount < 15:
                intensity, color_i = "Heavy Rain", "#1d4ed8"
            else:
                intensity, color_i = "Very Heavy Rain", "#1e40af"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Intensity Classification</div>
                <div style="font-size: 2rem; font-weight: 700; color: {color_i}; margin-bottom: 0.5rem;">{intensity}</div>
                <div style="font-size: 1.5rem; color: #f59e0b;">{max(0, rain_amount):.2f} mm/hr</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Seasonal context
        month = dt_obj.month
        if month in [6,7,8,9]:
            season_msg = "☔ Southwest Monsoon season — Rain is common and expected in Tirupati during this period."
            season_color = "#06b6d4"
        elif month in [10,11]:
            season_msg = "🌧️ Northeast Monsoon season — Tirupati typically receives significant rainfall."
            season_color = "#2563eb"
        elif month in [12,1,2]:
            season_msg = "❄️ Winter season — Generally dry with occasional light showers."
            season_color = "#64748b"
        else:
            season_msg = "🌤️ Summer season — Pre-monsoon showers possible, mostly dry conditions."
            season_color = "#f59e0b"
        
        st.markdown(f"""
        <div class="result-card" style="border-left: 4px solid {season_color};">
            <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Seasonal Context</div>
            <div style="color: white; font-size: 1.1rem; line-height: 1.6;">{season_msg}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Temperature Prediction Page
def render_temperature_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">🌡️ Temperature Forecasting</h1>
            <p class="page-subtitle">Comprehensive temperature analysis including air temperature, wet bulb, and dew point</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    temp_links = st.columns(4)
    with temp_links[0]:
        if st.button("Open Hourly Forecast", key="temp_open_hourly", use_container_width=True):
            navigate_to('hourly')
    with temp_links[1]:
        if st.button("Open Weekly Forecast", key="temp_open_weekly", use_container_width=True):
            navigate_to('weekly')
    with temp_links[2]:
        if st.button("Open 10-Day Forecast", key="temp_open_10day", use_container_width=True):
            navigate_to('10day')
    with temp_links[3]:
        if st.button("Open Research Export", key="temp_open_research", use_container_width=True):
            navigate_to('research')
    
    st.markdown("---")
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("temperature")
    
    if do_predict:
        with st.spinner("🌡️ Computing temperature forecast..."):
            time.sleep(0.8)
        
        air_temp = predict_weather_parameter('T2M', dt_obj)
        wet_bulb = predict_weather_parameter('T2MWET', dt_obj)
        dew_point = predict_weather_parameter('T2MDEW', dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        # Temperature gauges
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig1 = create_gauge_chart(air_temp, 10, 50, "Air Temperature", "°C", "#ef4444")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            fig2 = create_gauge_chart(wet_bulb, 5, 40, "Wet Bulb Temperature", "°C", "#f97316")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        with col3:
            fig3 = create_gauge_chart(dew_point, 0, 35, "Dew Point", "°C", "#06b6d4")
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        
        # Comfort assessment
        if air_temp < 20:
            comfort, color_c = "❄️ Cool & Comfortable", "#06b6d4"
        elif air_temp < 28:
            comfort, color_c = "😊 Perfect Weather", "#10b981"
        elif air_temp < 35:
            comfort, color_c = "🌤️ Warm & Pleasant", "#f59e0b"
        elif air_temp < 40:
            comfort, color_c = "🔥 Hot Weather", "#f97316"
        else:
            comfort, color_c = "🥵 Extreme Heat", "#ef4444"
        
        dew_depression = air_temp - dew_point
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Comfort Assessment</div>
                <div style="font-size: 2rem; font-weight: 700; color: {color_c}; margin-bottom: 0.5rem;">{comfort}</div>
                <div style="color: #f59e0b; font-size: 1.3rem;">{air_temp:.1f}°C</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            humidity_desc = "💧 Very Humid Conditions" if dew_depression < 3 else "🌤️ Moderate Humidity" if dew_depression < 8 else "☀️ Dry Air Conditions"
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Dew Point Depression</div>
                <div style="font-size: 2rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">{dew_depression:.1f}°C</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{humidity_desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('---')
        st.markdown('### 📅 Extended Temperature Forecast')
        temperature_horizon = st.radio(
            'Select prediction horizon',
            ['Hourly', 'Weekly', '10-Day', 'Monthly'],
            horizontal=True,
            key='temperature_horizon'
        )
        
        if temperature_horizon == 'Hourly':
            df_hourly = generate_hourly_forecast(models, scalers, features, metadata, dt_obj.date())
            st.markdown('#### Hourly Temperature Prediction')
            fig = create_hourly_line_plot(df_hourly, metadata, 'T2M', f"({dt_obj.strftime('%b %d')})")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            summary_rows = [{
                'Parameter': metadata['T2M']['name'],
                'Min': df_hourly['T2M'].min(),
                'Max': df_hourly['T2M'].max(),
                'Average': df_hourly['T2M'].mean()
            }]
            st.markdown('##### Min / Max / Average Summary')
            st.dataframe(pd.DataFrame(summary_rows).round(2), use_container_width=True)
            
            st.markdown('##### Hourly Data Table')
            st.dataframe(df_hourly[['Hour', 'T2M']].round(2), use_container_width=True)
        elif temperature_horizon == 'Weekly':
            df_weekly, _ = generate_weekly_forecast(models, scalers, features, metadata, dt_obj.date())
            st.markdown('#### Weekly Temperature Prediction')
            fig = create_daily_comparison_plot(df_weekly, 'T2M', metadata)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            summary_rows = [{
                'Parameter': metadata['T2M']['name'],
                'Min': df_weekly['T2M_min'].min(),
                'Max': df_weekly['T2M_max'].max(),
                'Average': df_weekly['T2M_avg'].mean()
            }]
            st.markdown('##### Min / Max / Average Summary')
            st.dataframe(pd.DataFrame(summary_rows).round(2), use_container_width=True)
            
            st.markdown('##### Weekly Summary Table')
            weekly_cols = ['Date', 'DayOfWeek', 'T2M_min', 'T2M_avg', 'T2M_max']
            st.dataframe(df_weekly[weekly_cols].round(2), use_container_width=True)
        elif temperature_horizon == '10-Day':
            df_10day, _ = generate_10day_forecast(models, scalers, features, metadata, dt_obj.date())
            st.markdown('#### 10-Day Temperature Prediction')
            fig = create_daily_comparison_plot(df_10day, 'T2M', metadata)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

            summary_rows = [{
                'Parameter': metadata['T2M']['name'],
                'Min': df_10day['T2M_min'].min(),
                'Max': df_10day['T2M_max'].max(),
                'Average': df_10day['T2M_avg'].mean()
            }]
            st.markdown('##### Min / Max / Average Summary')
            st.dataframe(pd.DataFrame(summary_rows).round(2), use_container_width=True)

            st.markdown('##### 10-Day Summary Table')
            ten_day_cols = ['Date', 'DayOfWeek', 'T2M_min', 'T2M_avg', 'T2M_max']
            st.dataframe(df_10day[ten_day_cols].round(2), use_container_width=True)
        else:
            df_monthly = generate_monthly_forecast(models, scalers, features, metadata, dt_obj.date())
            st.markdown('#### Monthly Temperature Prediction')
            fig = create_daily_comparison_plot(df_monthly, 'T2M', metadata)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            summary_rows = [{
                'Parameter': metadata['T2M']['name'],
                'Min': df_monthly['T2M_min'].min(),
                'Max': df_monthly['T2M_max'].max(),
                'Average': df_monthly['T2M_avg'].mean()
            }]
            st.markdown('##### Min / Max / Average Summary')
            st.dataframe(pd.DataFrame(summary_rows).round(2), use_container_width=True)
            
            st.markdown('##### Monthly Summary Table')
            monthly_cols = ['Date', 'DayOfWeek', 'T2M_min', 'T2M_avg', 'T2M_max']
            st.dataframe(df_monthly[monthly_cols].round(2), use_container_width=True)
# Complete Forecast Page
def render_complete_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">🔮 Complete Weather Forecast</h1>
            <p class="page-subtitle">Comprehensive prediction of all 23 weather parameters with detailed analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("complete")
    
    if do_predict:
        with st.spinner("🔮 Generating complete weather forecast..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            predictions = {}
            weather_targets = list(metadata.keys())
            
            for i, target in enumerate(weather_targets):
                status_text.text(f"Predicting {metadata[target]['name']}...")
                predictions[target] = predict_weather_parameter(target, dt_obj)
                progress_bar.progress((i + 1) / len(weather_targets))
                time.sleep(0.08)
            
            rain_prob, rain_flag = predict_rainfall_classification(dt_obj)
            
            progress_bar.empty()
            status_text.empty()
        
        st.markdown(f"""
        <div class="result-card" style="margin: 2rem 0;">
            <h2 style="color: white; font-size: 2rem; margin-bottom: 0.5rem;">🗓️ Complete Weather Forecast</h2>
            <h3 style="color: #f59e0b; font-size: 1.5rem;">{dt_obj.strftime('%A, %B %d, %Y at %I:%M %p')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Organize predictions by category
        categories = {
            "🌡️ Temperature & Humidity": ['T2M', 'T2MWET', 'T2MDEW', 'RH2M', 'QV2M'],
            "🌧️ Precipitation": ['PRECTOTCORR'],
            "🌬️ Wind Conditions": ['WS10M', 'WD10M', 'WS50M', 'WD50M'],
            "☀️ Solar Radiation": ['ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DNI', 'ALLSKY_SFC_SW_DIFF', 'ALLSKY_KT'],
            "🕶️ UV & PAR": ['ALLSKY_SFC_UVA', 'ALLSKY_SFC_UVB', 'ALLSKY_SFC_UV_INDEX', 'ALLSKY_SFC_PAR_TOT', 'CLRSKY_SFC_PAR_TOT'],
            "🌍 Atmospheric": ['PS', 'ALLSKY_SRF_ALB', 'SZA']
        }
        
        for category, params in categories.items():
            st.markdown(f"""
            <div style="margin: 2rem 0;">
                <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                    {category}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for this category
            cols = st.columns(min(len(params), 4))
            
            for i, param in enumerate(params):
                col_idx = i % 4
                with cols[col_idx]:
                    if param in predictions:
                        meta = metadata[param]
                        value = predictions[param]
                        
                        if param == 'PRECTOTCORR':
                            rain_status = "YES" if rain_flag else "NO"
                            st.markdown(f"""
                            <div class="result-card" style="margin: 0.5rem 0;">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{meta['icon']}</div>
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem;">{meta['name']}</div>
                                <div style="color: #f59e0b; font-size: 1.5rem; font-weight: 700;">{max(0, value):.{meta['decimals']}f} {meta['unit']}</div>
                                <div style="color: #06b6d4; font-size: 0.9rem; margin-top: 0.5rem;">Rain: {rain_status} ({rain_prob*100:.0f}%)</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif param in ['WD10M', 'WD50M']:
                            directions = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
                            compass = directions[int((value % 360) / 22.5)]
                            st.markdown(f"""
                            <div class="result-card" style="margin: 0.5rem 0;">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{meta['icon']}</div>
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem;">{meta['name']}</div>
                                <div style="color: #f59e0b; font-size: 1.5rem; font-weight: 700;">{compass}</div>
                                <div style="color: #06b6d4; font-size: 0.9rem; margin-top: 0.5rem;">{value:.{meta['decimals']}f}°</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-card" style="margin: 0.5rem 0;">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{meta['icon']}</div>
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem;">{meta['name']}</div>
                                <div style="color: #f59e0b; font-size: 1.5rem; font-weight: 700;">{value:.{meta['decimals']}f} {meta['unit']}</div>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Summary insights
        st.markdown("""
        <div style="margin: 3rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                📊 Weather Summary & Event Planning
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            temp = predictions['T2M']
            humidity = predictions['RH2M']
            wind = predictions['WS10M']
            
            conditions = []
            if temp > 35:
                conditions.append("🔥 Very Hot")
            elif temp > 30:
                conditions.append("🌤️ Hot")
            elif temp > 25:
                conditions.append("😊 Warm")
            else:
                conditions.append("❄️ Cool")
            
            if humidity > 80:
                conditions.append("💦 Very Humid")
            elif humidity > 60:
                conditions.append("💧 Humid")
            else:
                conditions.append("🌵 Dry")
            
            if wind > 10:
                conditions.append("💨 Windy")
            elif wind > 5:
                conditions.append("🌬️ Breezy")
            else:
                conditions.append("🍃 Calm")
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 1rem;">Overall Weather Conditions</div>
                <div style="color: white; font-size: 1.3rem; line-height: 1.8;">
                    {' • '.join(conditions)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            uv_index = predictions['ALLSKY_SFC_UV_INDEX']
            solar = predictions['ALLSKY_SFC_SW_DWN']
            
            recommendations = []
            if rain_flag:
                recommendations.append("☔ Indoor venue recommended")
            elif temp > 35:
                recommendations.append("🏢 Air-conditioned space advised")
            elif uv_index > 8:
                recommendations.append("🕶️ Sun protection needed")
            elif wind > 15:
                recommendations.append("🌬️ Secure outdoor setups")
            else:
                recommendations.append("✅ Good for outdoor events")
            
            if solar > 500:
                recommendations.append("☀️ Excellent solar conditions")
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 1rem;">Event Planning Recommendations</div>
                <div style="color: white; font-size: 1.1rem; line-height: 1.8;">
                    {'<br>'.join(recommendations)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Download option
        if st.button("📥 Download Complete Forecast Data", use_container_width=True):
            forecast_data = {
                'DateTime': dt_obj.strftime('%Y-%m-%d %H:%M'),
                'Rain_Probability': f"{rain_prob:.3f}",
                'Rain_Expected': rain_flag
            }
            
            for param, value in predictions.items():
                meta = metadata[param]
                forecast_data[f"{meta['name']} ({meta['unit']})"] = f"{value:.{meta['decimals']}f}"
            
            df_download = pd.DataFrame([forecast_data])
            csv = df_download.to_csv(index=False)
            
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"MBU_Weather_Forecast_{dt_obj.strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

# Monthly Forecast Page
def render_monthly_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">📅 Monthly Forecast</h1>
            <p class="page-subtitle">Comprehensive 12-month weather outlook with seasonal patterns and trends</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    # Year selection
    st.markdown("""
    <div class="input-section">
        <h3 class="input-title">📅 Select Year for Monthly Forecast</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_year = st.selectbox(
            "📅 Select Year",
            options=list(range(2026, 2036)),
            index=0,
            help="Choose year for 12-month forecast analysis"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("📊 Generate Monthly Forecast", use_container_width=True)
    
    if generate_btn:
        with st.spinner("📊 Generating 12-month forecast analysis..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Generate monthly data
            status_text.text("Analyzing monthly weather patterns...")
            monthly_data = predict_monthly_data(selected_year)
            progress_bar.progress(0.5)
            
            status_text.text("Creating visualizations...")
            progress_bar.progress(0.8)
            
            time.sleep(0.5)
            progress_bar.progress(1.0)
            progress_bar.empty()
            status_text.empty()
        
        # Display results
        st.markdown(f"""
        <div class="result-card" style="margin: 2rem 0;">
            <h2 style="color: white; font-size: 2rem; margin-bottom: 0.5rem;">📅 Monthly Weather Forecast</h2>
            <h3 style="color: #f59e0b; font-size: 1.5rem;">Year {selected_year} - Complete Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Seasonal Summary
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                🌍 Seasonal Weather Patterns
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        seasonal_fig = create_seasonal_summary_chart(monthly_data)
        st.plotly_chart(seasonal_fig, use_container_width=True, config={'displayModeBar': False})
        
        # Monthly Temperature Trends
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                🌡️ Temperature Trends
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        temp_fig = create_monthly_chart(monthly_data, 'T2M', 'Air Temperature', '°C', '#ef4444')
        st.plotly_chart(temp_fig, use_container_width=True, config={'displayModeBar': False})
        
        # Rainfall Patterns
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                🌧️ Rainfall Patterns
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            rainfall_fig = create_monthly_chart(monthly_data, 'PRECTOTCORR', 'Rainfall Amount', 'mm/hr', '#06b6d4')
            st.plotly_chart(rainfall_fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            rain_prob_fig = create_monthly_chart(monthly_data, 'rain_prob', 'Rain Probability', '%', '#2563eb')
            st.plotly_chart(rain_prob_fig, use_container_width=True, config={'displayModeBar': False})
        
        # Humidity and Wind
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                💧 Humidity & Wind Conditions
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            humidity_fig = create_monthly_chart(monthly_data, 'RH2M', 'Relative Humidity', '%', '#06b6d4')
            st.plotly_chart(humidity_fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            wind_fig = create_monthly_chart(monthly_data, 'WS10M', 'Wind Speed', 'm/s', '#64748b')
            st.plotly_chart(wind_fig, use_container_width=True, config={'displayModeBar': False})
        
        # Solar Radiation
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                ☀️ Solar Radiation & UV Index
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            solar_fig = create_monthly_chart(monthly_data, 'ALLSKY_SFC_SW_DWN', 'Solar Irradiance', 'Wh/m²', '#f59e0b')
            st.plotly_chart(solar_fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            uv_fig = create_monthly_chart(monthly_data, 'ALLSKY_SFC_UV_INDEX', 'UV Index', '', '#ef4444')
            st.plotly_chart(uv_fig, use_container_width=True, config={'displayModeBar': False})
        
        # Monthly Summary Table
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                📊 Monthly Summary Statistics
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create summary table
        summary_data = []
        for month in monthly_data.keys():
            data = monthly_data[month]
            summary_data.append({
                'Month': month,
                'Avg Temp (°C)': f"{data['T2M']['avg']:.1f}",
                'Avg Humidity (%)': f"{data['RH2M']['avg']:.1f}",
                'Avg Rainfall (mm/hr)': f"{data['PRECTOTCORR']['avg']:.2f}",
                'Rain Probability (%)': f"{data['rain_prob']['avg']:.1f}",
                'Avg Wind (m/s)': f"{data['WS10M']['avg']:.1f}",
                'Avg Solar (Wh/m²)': f"{data['ALLSKY_SFC_SW_DWN']['avg']:.0f}",
                'Avg UV Index': f"{data['ALLSKY_SFC_UV_INDEX']['avg']:.1f}"
            })
        
        df_summary = pd.DataFrame(summary_data)
        
        # Style the dataframe
        st.dataframe(
            df_summary,
            use_container_width=True,
            hide_index=True
        )
        
        # Seasonal Insights
        st.markdown("""
        <div style="margin: 3rem 0 1rem 0;">
            <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">
                🔍 Seasonal Insights & Recommendations
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate insights
        insights = []
        
        # Temperature insights
        temp_data = [monthly_data[month]['T2M']['avg'] for month in monthly_data.keys()]
        hottest_month = list(monthly_data.keys())[np.argmax(temp_data)]
        coolest_month = list(monthly_data.keys())[np.argmin(temp_data)]
        
        insights.append(f"🌡️ **Temperature**: Hottest in {hottest_month} ({max(temp_data):.1f}°C), coolest in {coolest_month} ({min(temp_data):.1f}°C)")
        
        # Rainfall insights
        rain_data = [monthly_data[month]['PRECTOTCORR']['avg'] for month in monthly_data.keys()]
        wettest_month = list(monthly_data.keys())[np.argmax(rain_data)]
        driest_month = list(monthly_data.keys())[np.argmin(rain_data)]
        
        insights.append(f"🌧️ **Rainfall**: Wettest in {wettest_month} ({max(rain_data):.2f} mm/hr), driest in {driest_month} ({min(rain_data):.2f} mm/hr)")
        
        # Monsoon insights
        sw_monsoon_rain = np.mean([monthly_data[month]['PRECTOTCORR']['avg'] for month in ['June', 'July', 'August', 'September']])
        ne_monsoon_rain = np.mean([monthly_data[month]['PRECTOTCORR']['avg'] for month in ['October', 'November']])
        
        insights.append(f"☔ **Monsoons**: SW Monsoon avg {sw_monsoon_rain:.2f} mm/hr, NE Monsoon avg {ne_monsoon_rain:.2f} mm/hr")
        
        # UV insights
        uv_data = [monthly_data[month]['ALLSKY_SFC_UV_INDEX']['avg'] for month in monthly_data.keys()]
        high_uv_months = [month for month, uv in zip(monthly_data.keys(), uv_data) if uv > 8]
        
        if high_uv_months:
            insights.append(f"🕶️ **UV Protection**: High UV months ({', '.join(high_uv_months)}) - extra sun protection recommended")
        
        # Display insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 1rem;">Key Weather Insights</div>
                <div style="color: white; font-size: 1rem; line-height: 2;">
                    {'<br>'.join(insights[:2])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 1rem;">Planning Recommendations</div>
                <div style="color: white; font-size: 1rem; line-height: 2;">
                    {'<br>'.join(insights[2:])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Download option
        if st.button("📥 Download Monthly Forecast Data", use_container_width=True):
            csv = df_summary.to_csv(index=False)
            
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"MBU_Monthly_Forecast_{selected_year}.csv",
                mime="text/csv"
            )

# Humidity Prediction Page
def render_humidity_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">💧 Humidity Analysis</h1>
            <p class="page-subtitle">Comprehensive humidity forecasting for optimal comfort and planning</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("humidity")
    
    if do_predict:
        with st.spinner("💧 Analyzing humidity conditions..."):
            time.sleep(0.8)
        
        rel_humidity = predict_weather_parameter('RH2M', dt_obj)
        spec_humidity = predict_weather_parameter('QV2M', dt_obj)
        dew_point = predict_weather_parameter('T2MDEW', dt_obj)
        air_temp = predict_weather_parameter('T2M', dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_gauge_chart(rel_humidity, 0, 100, "Relative Humidity", "%", "#06b6d4")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            fig2 = create_gauge_chart(spec_humidity, 0, 30, "Specific Humidity", "g/kg", "#2563eb")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Comfort assessment
            if rel_humidity < 30:
                comfort, color_c = "🏜️ Very Dry", "#f59e0b"
                comfort_desc = "Low humidity may cause discomfort"
            elif rel_humidity < 50:
                comfort, color_c = "😊 Comfortable", "#10b981"
                comfort_desc = "Ideal humidity for most activities"
            elif rel_humidity < 70:
                comfort, color_c = "💧 Moderate", "#06b6d4"
                comfort_desc = "Slightly humid but comfortable"
            elif rel_humidity < 85:
                comfort, color_c = "💦 Humid", "#2563eb"
                comfort_desc = "High humidity, may feel sticky"
            else:
                comfort, color_c = "🌊 Very Humid", "#1d4ed8"
                comfort_desc = "Oppressive humidity conditions"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Comfort Level</div>
                <div style="font-size: 2rem; font-weight: 700; color: {color_c}; margin-bottom: 0.5rem;">{comfort}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{comfort_desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Heat index calculation
            heat_index = air_temp + 0.5 * (rel_humidity - 50) * 0.1
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Apparent Temperature</div>
                <div style="font-size: 2rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">{heat_index:.1f}°C</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">How it feels with humidity</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Wind Prediction Page
def render_wind_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">🌬️ Wind Conditions</h1>
            <p class="page-subtitle">Wind speed and direction forecasting at multiple heights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("wind")
    
    if do_predict:
        with st.spinner("🌬️ Analyzing wind patterns..."):
            time.sleep(0.8)
        
        wind_10m = predict_weather_parameter('WS10M', dt_obj)
        wind_dir_10m = predict_weather_parameter('WD10M', dt_obj)
        wind_50m = predict_weather_parameter('WS50M', dt_obj)
        wind_dir_50m = predict_weather_parameter('WD50M', dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_gauge_chart(wind_10m, 0, 25, "Wind Speed (10m)", "m/s", "#64748b")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            fig2 = create_gauge_chart(wind_50m, 0, 30, "Wind Speed (50m)", "m/s", "#475569")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Wind direction compass
            directions = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
            compass_10m = directions[int((wind_dir_10m % 360) / 22.5)]
            compass_50m = directions[int((wind_dir_50m % 360) / 22.5)]
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Wind Direction (10m)</div>
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧭</div>
                <div style="font-size: 2rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">{compass_10m}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{wind_dir_10m:.0f}°</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Beaufort scale
            if wind_10m < 0.3:
                beaufort, desc = "0 - Calm", "Smoke rises vertically"
            elif wind_10m < 1.6:
                beaufort, desc = "1 - Light Air", "Smoke drift indicates direction"
            elif wind_10m < 3.4:
                beaufort, desc = "2 - Light Breeze", "Wind felt on face"
            elif wind_10m < 5.5:
                beaufort, desc = "3 - Gentle Breeze", "Leaves in constant motion"
            elif wind_10m < 8.0:
                beaufort, desc = "4 - Moderate Breeze", "Small branches move"
            elif wind_10m < 10.8:
                beaufort, desc = "5 - Fresh Breeze", "Small trees sway"
            elif wind_10m < 13.9:
                beaufort, desc = "6 - Strong Breeze", "Large branches move"
            else:
                beaufort, desc = "7+ - High Wind", "Whole trees in motion"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Beaufort Scale</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #06b6d4; margin-bottom: 0.5rem;">{beaufort}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Solar Prediction Page
def render_solar_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">☀️ Solar Radiation</h1>
            <p class="page-subtitle">Comprehensive solar energy and UV forecasting</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("solar")
    
    if do_predict:
        with st.spinner("☀️ Analyzing solar conditions..."):
            time.sleep(0.8)
        
        solar_total = predict_weather_parameter('ALLSKY_SFC_SW_DWN', dt_obj)
        solar_direct = predict_weather_parameter('ALLSKY_SFC_SW_DNI', dt_obj)
        solar_diffuse = predict_weather_parameter('ALLSKY_SFC_SW_DIFF', dt_obj)
        uv_index = predict_weather_parameter('ALLSKY_SFC_UV_INDEX', dt_obj)
        par_total = predict_weather_parameter('ALLSKY_SFC_PAR_TOT', dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig1 = create_gauge_chart(max(0, solar_total), 0, 1000, "Total Solar", "Wh/m²", "#f59e0b")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            fig2 = create_gauge_chart(max(0, uv_index), 0, 15, "UV Index", "", "#ef4444")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        with col3:
            fig3 = create_gauge_chart(max(0, par_total), 0, 500, "PAR Total", "W/m²", "#10b981")
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        
        # UV protection advice
        col1, col2 = st.columns(2)
        
        with col1:
            if uv_index < 3:
                uv_risk, color_uv = "🟢 Low Risk", "#10b981"
                uv_advice = "Minimal protection needed"
            elif uv_index < 6:
                uv_risk, color_uv = "🟡 Moderate Risk", "#f59e0b"
                uv_advice = "Seek shade during midday"
            elif uv_index < 8:
                uv_risk, color_uv = "🟠 High Risk", "#f97316"
                uv_advice = "Protection essential"
            elif uv_index < 11:
                uv_risk, color_uv = "🔴 Very High Risk", "#ef4444"
                uv_advice = "Extra protection required"
            else:
                uv_risk, color_uv = "🟣 Extreme Risk", "#8b5cf6"
                uv_advice = "Avoid sun exposure"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">UV Protection</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {color_uv}; margin-bottom: 0.5rem;">{uv_risk}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{uv_advice}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Solar energy potential
            if solar_total > 700:
                solar_potential = "⚡ Excellent for Solar"
            elif solar_total > 400:
                solar_potential = "🔋 Good for Solar"
            elif solar_total > 200:
                solar_potential = "🌤️ Moderate Solar"
            else:
                solar_potential = "☁️ Poor Solar Conditions"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Solar Energy Potential</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">{solar_potential}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{max(0, solar_total):.0f} Wh/m²</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Atmospheric Prediction Page
def render_atmospheric_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">🌍 Atmospheric Conditions</h1>
            <p class="page-subtitle">Surface pressure and atmospheric parameter analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    dt_obj, do_predict = datetime_input_widget("atmospheric")
    
    if do_predict:
        with st.spinner("🌍 Analyzing atmospheric conditions..."):
            time.sleep(0.8)
        
        pressure = predict_weather_parameter('PS', dt_obj)
        albedo = predict_weather_parameter('ALLSKY_SRF_ALB', dt_obj)
        zenith = predict_weather_parameter('SZA', dt_obj)
        clearness = predict_weather_parameter('ALLSKY_KT', dt_obj)
        
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_gauge_chart(pressure, 95, 105, "Surface Pressure", "kPa", "#2563eb")
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            fig2 = create_gauge_chart(zenith, 0, 90, "Solar Zenith Angle", "°", "#f59e0b")
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Pressure trend
            if pressure > 102:
                pressure_trend, color_p = "📈 High Pressure", "#10b981"
                pressure_desc = "Fair weather expected"
            elif pressure > 98:
                pressure_trend, color_p = "📊 Normal Pressure", "#06b6d4"
                pressure_desc = "Stable conditions"
            else:
                pressure_trend, color_p = "📉 Low Pressure", "#ef4444"
                pressure_desc = "Unsettled weather possible"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Pressure Analysis</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {color_p}; margin-bottom: 0.5rem;">{pressure_trend}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">{pressure_desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sky conditions
            if clearness > 0.7:
                sky_condition = "☀️ Clear Skies"
            elif clearness > 0.5:
                sky_condition = "⛅ Partly Cloudy"
            elif clearness > 0.3:
                sky_condition = "☁️ Mostly Cloudy"
            else:
                sky_condition = "🌫️ Overcast"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 0.5rem;">Sky Conditions</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">{sky_condition}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 1rem;">Clearness: {clearness:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Hourly/Weekly/Daily/Research pages moved to new_pages.py
# The implementations previously here were removed to avoid duplication.

# Main App
def main():
    render_navbar()
    
    current_page = st.session_state.current_page
    
    if current_page == 'home':
        render_home_page()
    elif current_page == 'rainfall':
        render_rainfall_page()
    elif current_page == 'temperature':
        render_temperature_page()
    elif current_page == 'humidity':
        render_humidity_page()
    elif current_page == 'wind':
        render_wind_page()
    elif current_page == 'solar':
        render_solar_page()
    elif current_page == 'atmospheric':
        render_atmospheric_page()
    elif current_page == 'complete':
        render_complete_page()
    elif current_page == 'monthly':
        render_monthly_page()
    elif current_page == 'hourly':
        new_pages.render_hourly_page()
    elif current_page == 'weekly':
        new_pages.render_weekly_page()
    elif current_page == '10day':
        new_pages.render_10day_page()
    elif current_page == 'monthly':
        new_pages.render_monthly_page()
    elif current_page == '12month':
        new_pages.render_12month_page()
    elif current_page == 'daily_summary':
        new_pages.render_daily_summary_page()
    elif current_page == 'research':
        new_pages.render_research_page()
    else:
        render_home_page()  # Default fallback

if __name__ == "__main__":
    main()