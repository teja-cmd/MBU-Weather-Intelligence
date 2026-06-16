# 🌤️ MBU Weather Intelligence System

**Advanced AI-Powered Weather Prediction System for Mohan Babu University, Tirupati**

## 🎯 Project Overview

This advanced weather prediction system helps Mohan Babu University plan outdoor events, campus activities, and academic programs by forecasting weather conditions for any future date and time using machine learning models trained on 10+ years of NASA POWER data.

## ✨ New Features (Latest Update)

### 🆕 **Advanced Forecast Capabilities:**
- **⏰ 24-Hour Hourly Forecast** - Detailed hourly predictions with interactive line plots, multi-parameter charts, and heatmaps
- **📅 7-Day Weekly Forecast** - Long-term predictions with daily min/max/average aggregates and trending visualizations
- **� Monthly Forecast** - Comprehensive 12-month weather outlook with seasonal patterns, trends, and statistical analysis
- **�📊 Daily Summary with Max/Min** - Aggregated daily predictions showing maximum, minimum, and average values for all parameters
- **📑 Research Paper Export** - Export model metrics, performance statistics (R², MAE, RMSE), and comprehensive research reports in JSON/CSV/TXT formats

### 🚀 **Improved Model Performance:**
- **Hyperparameter Tuning:** GridSearchCV and RandomizedSearchCV for optimized models
- **Better R² Scores:** Enhanced model configurations for each weather parameter
- **Early Stopping:** Implemented for XGBoost models to prevent overfitting
- **Ensemble Methods:** Optimized RandomForest parameters for directional parameters
- **Target-Specific Optimization:** Unique hyperparameters per weather parameter type

### 🎨 **Enhanced Visualizations:**
- **Line Plots:** Interactive hourly trends with smooth lines and markers
- **Multi-Parameter Charts:** Compare multiple weather variables on one plot
- **Heatmaps:** Normalized visualization of all parameters across 24 hours
- **Daily Comparison:** Min/max/average bands for weekly forecasts
- **Monthly Trends:** Seasonal patterns with min/max ranges and statistical insights
- **Seasonal Radar Charts:** Comparative analysis of weather patterns across seasons
- **Gauge Charts:** Real-time parameter display with color-coded ranges

### 📊 **Rich Exports for Research:**
- **JSON Export:** Structured data with model metrics
- **CSV Export:** Tabular format for Excel and analysis tools
- **Research Reports:** Formatted text with methodology, results, and recommendations
- **Model Statistics:** Average R², MAE, RMSE across all trained models

## 🔮 **23 Weather Parameters Predicted:**
- **🌡️ Temperature:** Air, Wet Bulb, Dew Point
- **💧 Humidity:** Relative & Specific Humidity  
- **🌧️ Rainfall:** Amount & Probability Classification
- **🌬️ Wind:** Speed & Direction (10m & 50m heights)
- **☀️ Solar Radiation:** All-sky, Clear-sky, Direct, Diffuse
- **🕶️ UV & PAR:** UVA, UVB, UV Index, Photosynthetic Radiation
- **🌍 Atmospheric:** Pressure, Albedo, Solar Zenith Angle

## 🎨 **Beautiful UI Features:**
- **Modern Dashboard** with animated weather theme and gradient backgrounds
- **Interactive Gauges** and real-time charts with professional styling
- **Complete Model Pages** for all weather categories (Temperature, Humidity, Wind, Solar, Atmospheric, Rainfall)
- **Complete Forecast** with all 23 parameters in one comprehensive view
- **Professional Navigation** with smooth animations and glass-morphism effects
- **Event Planning Recommendations** based on weather conditions
- **Multi-Format Data Export** (CSV, JSON, TXT) for detailed analysis
- **Responsive Design** that works perfectly on all devices
- **Custom Color Scheme** with beautiful gradients and professional styling

## 🚀 Quick Start

### **Option 1: One-Click Start (Recommended)**
```bash
python start_app.py
```
*This will automatically train models if needed and start the app*

### **Option 2: Automatic Setup**
```bash
python setup.py
streamlit run app.py
```

### **Option 3: Manual Setup**

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Train Models (with optimizations):**
```bash
python train_models.py
```
*Note: This will perform hyperparameter tuning and may take 15-20 minutes*

3. **Run Application:**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
mbu-weather/
├── app.py                      # Main Streamlit application
├── train_models.py             # ML training with hyperparameter tuning
├── forecast_utils.py           # Forecasting and visualization utilities
├── start_app.py                # One-click startup script
├── data.csv                    # NASA POWER dataset
├── requirements.txt            # Python dependencies
├── setup.py                    # Automatic setup script
├── README.md                   # This file
├── train_models_old.py         # Original training script (backup)
└── models/                     # Trained ML models (auto-generated)
    ├── T2M_model.pkl           # Temperature model
    ├── RH2M_model.pkl          # Humidity model
    ├── PRECTOTCORR_model.pkl   # Rainfall model
    ├── RAIN_classifier.pkl     # Rain classification
    ├── model_results.pkl       # Performance metrics
    ├── weather_metadata.pkl    # Parameter metadata
    └── ... (all 23 models + scalers)
```

## 📖 How to Use

### **1. Single-Time Predictions:**
- Select a weather model (Temperature, Rainfall, Humidity, etc.)
- Choose a future date and time
- View real-time predictions with beautiful gauge charts

### **2. Hourly Forecasts:**
- Go to "Hourly Forecast" page
- Select any date
- Choose visualization type (Line Plot, Multi-Parameter, Heatmap)
- Download hourly data as CSV

### **3. Weekly Forecasts:**
- Go to "Weekly Forecast" page
- Select start date
- View 7-day predictions with daily min/max/average
- Track trends across the week

### **4. Daily Summaries:**
- Go to "Daily Summary" page
- Select a date
- See aggregated max/min/average for key parameters

### **5. Monthly Forecasts:**
- Go to "Monthly Forecast" page
- Select a year (2026-2035)
- View comprehensive 12-month analysis with:
  - Seasonal weather patterns (radar chart)
  - Monthly temperature, rainfall, humidity, and wind trends
  - Solar radiation and UV index patterns
  - Statistical summary table with averages
  - Seasonal insights and planning recommendations
- Download monthly data as CSV

### **6. Research Exports:**
- Go to "Research Export" page
- View model performance metrics
- Export data in JSON, CSV, or research report format
- Use for academic papers and publications

## 🎓 University Use Cases

### **Event Planning:**
- **🎓 Graduations:** Check temperature, rain, wind conditions for 3-4 weeks ahead
- **🏆 Sports Events:** Analyze hourly weather for optimal timing
- **🎭 Cultural Programs:** Plan indoor/outdoor venues with confidence
- **📚 Academic Conferences:** Ensure optimal conditions for multi-day events

### **Campus Operations:**
- **🔧 Maintenance:** Schedule based on weather forecasts
- **⚡ Energy Management:** Predict solar and temperature patterns for load planning
- **🚨 Safety Planning:** Monitor extreme weather conditions
- **🌱 Research Support:** Environmental data for ecological and atmospheric studies

### **Academic Research:**
- **Export model metrics** for publication in weather prediction journals
- **Use forecasts** for climate impact studies
- **Analyze trends** with comprehensive historical data
- **Benchmark models** against university weather station

## 🤖 Machine Learning Details

### **Models Used:**
- **XGBoost Regressor:** For most weather parameters with hyperparameter optimization
- **Random Forest:** For wind direction and classification with optimized depth
- **Standard Scaler:** Feature normalization for all models
- **Time-based Features:** 26 engineered cyclical and seasonal features

### **Hyperparameter Optimization:**
- **XGBoost:** Learning rate tuning, tree depth optimization, gamma adjustment
- **RandomForest:** Ensemble size (150-300 trees), max depth (8-15), split/leaf optimization
- **Early Stopping:** Implemented for gradient boosting models
- **Target-Specific Tuning:** Rainfall uses deeper trees (8), temperature uses moderate depth (7)

### **Performance Metrics:**
All models evaluated on 20% test set (2022-2026 data):
- **Temperature:** R² = ~0.80-0.85
- **Humidity:** R² = ~0.75-0.80
- **Solar Radiation:** R² = ~0.78-0.82
- **Wind Speed:** R² = ~0.72-0.76
- **Rainfall Classifier:** ~60-65% Accuracy
- **Training Data:** 97K+ hourly records (2015-2026)

## 🌍 Climate Context

**Tirupati-Specific Features:**
- **Southwest Monsoon:** June-September (High rainfall, 500+ mm)
- **Northeast Monsoon:** October-November (Moderate rainfall)
- **Summer Season:** March-May (Hot, 35-40°C, dry)
- **Winter Season:** December-February (Cool, 20-25°C, dry)
- **Latitude:** 13.1939°N | **Longitude:** 79.8941°E

## 📊 Technical Specifications

### **Input Features (26 Time-Based):**
- Date/Time components (year, month, day, hour, day of week, etc.)
- Cyclical encodings (sin/cos for hour, month, day of year)
- Seasonal indicators (monsoon seasons, climate zones)
- Diurnal patterns (daytime, peak solar, night hours)
- Long-term trend (year trend from 2015)

### **Output Data:**
- Real-time predictions for 2026-2035
- Interactive visualizations (gauges, charts, heatmaps)
- Event planning recommendations
- Downloadable forecast data (CSV, JSON, TXT)
- Research-ready statistics and metrics

### **Forecast Horizons:**
- **Single Point:** Any specific date/time from 2026-2035
- **Hourly:** 24-hour detailed forecasts
- **Daily:** Aggregated min/max/average values
- **Weekly:** 7-day trend analysis
- **Monthly:** 12-month seasonal patterns and statistical analysis

## 🎨 UI Features

The system features a professional interface with:
- **Animated gradient backgrounds** with weather-themed colors
- **Interactive gauge visualizations** for each parameter
- **Responsive grid layouts** that work on all devices
- **Smooth CSS animations** and transitions
- **Professional color palette** (blues, oranges, greens)
- **Glass-morphism effects** for modern aesthetic

## ⚠️ Important Notes

### **Prediction Range:**
- **Future Dates:** 2026-2035 (based on climatological patterns)
- **Historical Training:** 2015-present NASA POWER satellite data
- **Seasonal Accuracy:** Highest accuracy for seasonal patterns

### **Accuracy & Limitations:**
- Predictions based on 10+ years of historical climate patterns
- For critical events, also consult real-time weather forecasts
- Best used for long-term planning (weeks to months ahead)
- Does not account for extreme weather events or climate anomalies

### **Data Quality:**
- **No gaps:** Continuous hourly data from NASA POWER
- **Quality checked:** Removed outliers and invalid records
- **Standardized:** All values in SI units

## 🔧 Troubleshooting

### **Common Issues:**

1. **Models not loading:**
   ```bash
   python train_models.py
   ```
   *This will retrain all models with optimizations*

2. **Slow training (hyperparameter tuning):**
   - Expected: 15-20 minutes for full optimization
   - You can stop and restart anytime (models save incrementally)

3. **Import errors:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Out of memory (large forecasts):**
   - Reduce forecast range or generate one week at a time

## 📈 Future Enhancements

- **Real-time data integration** with Weather APIs (OpenWeatherMap, etc.)
- **Historical comparison** features and anomaly detection
- **Mobile app** development (iOS/Android)
- **Advanced mapping** with geographical visualization
- **Email alerts** for extreme weather conditions
- **Integration** with university calendar and event systems
- **Prediction uncertainty** estimates (confidence intervals)
- **Seasonal forecasts** (3-6 month ahead)

## 🎉 Key Achievements

This enhanced system provides:

✅ **Better Accuracy:** Optimized models with hyperparameter tuning  
✅ **Flexible Forecasting:** Single-point, hourly, daily, and weekly predictions  
✅ **Rich Visualizations:** Multiple chart types for comprehensive analysis  
✅ **Research-Ready:** Export metrics and statistics for academic publications  
✅ **Scalable Architecture:** Modular design for easy extensions  
✅ **Professional UI:** Modern, responsive, and beautiful interface  
✅ **Complete Documentation:** Clear guides for all features  

---

## 📚 References

- **NASA POWER:** https://power.larc.nasa.gov/
- **XGBoost:** https://xgboost.readthedocs.io/
- **Streamlit:** https://streamlit.io/
- **Scikit-learn:** https://scikit-learn.org/

---

**🌤️ MBU Weather Intelligence System - v2.0**

*Advanced AI-Powered Weather Prediction & Research Export*

*Developed for Mohan Babu University, Tirupati*  
*Last Updated: May 2026*
