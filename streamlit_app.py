#!/usr/bin/env python3
"""
MBU Weather Intelligence - Streamlit Cloud Entry Point
====================================================
Optimized entry point for Streamlit Cloud deployment
"""

import os
import sys
import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="MBU Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_model_files():
    """Check if model files exist"""
    models_dir = 'models'
    if not os.path.exists(models_dir):
        return False, "Models directory not found"
    
    essential_files = [
        'weather_metadata.pkl',
        'weather_targets.pkl', 
        'feature_names.pkl'
    ]
    
    missing_files = []
    for file in essential_files:
        if not os.path.exists(os.path.join(models_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        return False, f"Missing files: {', '.join(missing_files)}"
    
    return True, "Models available"

# Check models and show appropriate interface
models_available, message = check_model_files()

if models_available:
    # Import and run the main application
    try:
        from app import *
        
    except ImportError as e:
        st.error(f"Import Error: {e}")
        st.info("Please ensure all required packages are installed.")
        
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("There was an error loading the application. Please try refreshing the page.")
        
else:
    # Show information page when models are not available
    st.markdown("""
    # 🌤️ MBU Weather Intelligence System
    
    **Advanced AI-Powered Weather Prediction System**  
    *Developed for Mohan Babu University, Tirupati*
    
    ---
    
    ## 🚧 System Status
    
    The machine learning models are currently being loaded. This is normal for the first deployment.
    
    ### ⚠️ Current Issue:
    """)
    
    st.warning(f"**{message}**")
    
    st.markdown("""
    ### 🔄 Next Steps:
    
    1. **Model Training**: The system needs to train machine learning models first
    2. **Data Processing**: Processing 97K+ weather data points from NASA POWER
    3. **Model Generation**: Creating 23 specialized weather prediction models
    
    ### 📊 System Features (Available after setup):
    
    - **24-Hour Hourly Forecast** - Detailed hourly predictions
    - **7-Day Weekly Forecast** - Week-long weather outlook  
    - **Monthly Predictions** - Long-term weather patterns
    - **Complete Weather Analysis** - 23 meteorological parameters
    - **Research Export** - Academic data export capabilities
    
    ### 🎓 About This Project
    
    This system predicts weather conditions for Mohan Babu University using:
    - **NASA POWER satellite data** (2015-present)
    - **Advanced ML models** (XGBoost, Random Forest)
    - **97K+ data points** for training
    - **23 weather parameters** including temperature, humidity, rainfall, wind, solar radiation
    
    ---
    
    ### 👨‍💻 Developer
    
    **Bathula Teja Kumar**  
    AIML Student, 2023-2027 Batch  
    Mohan Babu University
    
    ---
    
    *The system will be fully functional once the initial model training is complete.*
    """)
    
    # Show some demo visualizations
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    
    st.markdown("### 📈 Preview: System Capabilities")
    
    # Demo chart
    dates = pd.date_range(start='2026-06-17', periods=7)
    temp_data = np.random.normal(28, 3, 7)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=temp_data,
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#f59e0b', width=3)
    ))
    
    fig.update_layout(
        title="Sample: 7-Day Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)