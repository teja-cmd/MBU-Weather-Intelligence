#!/usr/bin/env python3
"""
MBU Weather Intelligence - Streamlit Cloud Entry Point
====================================================
Optimized entry point for Streamlit Cloud deployment
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configure Streamlit page FIRST
st.set_page_config(
    page_title="MBU Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for better styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426 0%, #0b1f2f 50%, #071426 100%);
}

.main > div {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #f8fafc;
}

.stMarkdown {
    color: #e2e8f0;
}

.highlight-box {
    background: rgba(139, 92, 246, 0.1);
    border-left: 4px solid #8b5cf6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

.developer-box {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 1.5rem;
    border-radius: 0.75rem;
    text-align: center;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    # 🌤️ MBU Weather Intelligence System
    
    **Advanced AI-Powered Weather Prediction System**  
    *Developed for Mohan Babu University, Tirupati*
    
    ---
    """)
    
    # Status section
    st.markdown("""
    <div class="highlight-box">
    <h2>🚀 System Status: LIVE!</h2>
    <p>Welcome to the MBU Weather Intelligence System! This application provides comprehensive weather predictions using advanced machine learning models trained on NASA POWER data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌟 Core Features:
        
        - 🌡️ **Temperature Forecasting** - Air, wet bulb, and dew point
        - 🌧️ **Rainfall Prediction** - Probability and intensity analysis  
        - 💧 **Humidity Analysis** - Relative and specific humidity
        - 🌬️ **Wind Conditions** - Speed and direction forecasting
        - ☀️ **Solar Radiation** - UV index and irradiance
        - 📅 **Multi-timeframe** - Hourly, daily, weekly, monthly
        """)
    
    with col2:
        st.markdown("""
        ### 📊 System Capabilities:
        
        - **97K+ Data Points** from NASA POWER
        - **23 Weather Parameters** predicted
        - **10+ Years** of training data
        - **Advanced ML Models** (XGBoost, Random Forest)
        - **High Accuracy** predictions for Tirupati
        - **Research Export** capabilities
        """)
    
    # Sample visualizations
    st.markdown("### 📈 Sample Weather Data Visualization")
    
    # Generate sample 7-day forecast data
    dates = [datetime.now() + timedelta(days=i) for i in range(7)]
    temperatures = [28.5, 31.2, 29.8, 32.1, 30.5, 27.9, 26.8]
    humidity = [65, 72, 68, 70, 75, 80, 78]
    
    # Temperature Chart
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=[d.strftime('%a %d') for d in dates],
            y=temperatures,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8, color='#f59e0b')
        ))
        
        fig_temp.update_layout(
            title="🌡️ 7-Day Temperature Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_humidity = go.Figure()
        fig_humidity.add_trace(go.Bar(
            x=[d.strftime('%a %d') for d in dates],
            y=humidity,
            name='Humidity (%)',
            marker_color='#06b6d4'
        ))
        
        fig_humidity.update_layout(
            title="💧 7-Day Humidity Forecast",
            xaxis_title="Date",
            yaxis_title="Humidity (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Use cases
    st.markdown("""
    ### 🎯 Use Cases for MBU:
    
    - **🎓 Event Planning** - Schedule graduations, sports events, cultural programs
    - **🏢 Campus Operations** - Optimize maintenance and energy management
    - **📚 Academic Research** - Export data for climate and environmental studies
    - **⚠️ Safety Planning** - Monitor extreme weather conditions
    - **🌱 Agricultural Research** - Support farming and horticulture programs
    """)
    
    # System status
    st.markdown("""
    ### 🔄 Current Development Status:
    
    The system is currently being optimized for cloud deployment. The machine learning models 
    trained on 97K+ NASA POWER data points are being prepared for the production environment.
    
    **Technical Implementation:**
    - Framework: Streamlit for web interface
    - ML Libraries: XGBoost, scikit-learn, pandas
    - Visualization: Plotly for interactive charts
    - Data Source: NASA POWER meteorological database
    - Deployment: Streamlit Cloud for global accessibility
    """)
    
    # Geographic info
    st.markdown("""
    ### 🌍 Geographic Context
    
    - **Location**: Tirupati, Andhra Pradesh, India
    - **Coordinates**: 13.1939°N, 79.8941°E  
    - **Climate**: Tropical savanna with distinct monsoon seasons
    - **Elevation**: 182 meters above sea level
    - **Weather Patterns**: SW Monsoon (Jun-Sep), NE Monsoon (Oct-Nov)
    """)
    
    # Developer section
    st.markdown("""
    <div class="developer-box">
    <h3>👨‍💻 Project Developer</h3>
    <h2 style="color: #f59e0b; margin: 0.5rem 0;">Bathula Teja Kumar</h2>
    <p><strong>AIML Student, 2023-2027 Batch</strong><br>
    <strong>Mohan Babu University</strong></p>
    <p><em>Specializing in Machine Learning and Weather Prediction Systems</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    
    **🌤️ MBU Weather Intelligence System**  
    *Empowering Smart Campus Decisions Through AI*
    
    *System Version: 2.0 | Deployed: June 2026*
    
    ---
    
    🏛️ **About Mohan Babu University**: Located in Tirupati, Andhra Pradesh, 
    Mohan Babu University is a leading institution focused on innovation in 
    technology and education. This weather intelligence system demonstrates 
    the university's commitment to practical applications of AI and machine learning.
    """)

if __name__ == "__main__":
    main()