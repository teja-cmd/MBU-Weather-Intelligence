#!/usr/bin/env python3
"""
MBU Weather Intelligence - Complete ML Training with Hyperparameter Tuning
==========================================================================
Train all weather prediction models with optimized hyperparameters for better R² scores
"""

import pandas as pd
import numpy as np
import joblib
import os
import warnings
from datetime import datetime
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import xgboost as xgb

warnings.filterwarnings('ignore')

def create_time_features(df_input):
    """Create comprehensive time-based features"""
    d = df_input.copy()
    dt = d['DATETIME']
    
    # Basic time components
    d['year'] = dt.dt.year
    d['month'] = dt.dt.month
    d['day'] = dt.dt.day
    d['hour'] = dt.dt.hour
    d['day_of_year'] = dt.dt.dayofyear
    d['day_of_week'] = dt.dt.dayofweek
    d['week_of_year'] = dt.dt.isocalendar().week.astype(int)
    d['quarter'] = dt.dt.quarter
    
    # Cyclical encodings
    d['hour_sin'] = np.sin(2 * np.pi * d['hour'] / 24)
    d['hour_cos'] = np.cos(2 * np.pi * d['hour'] / 24)
    d['month_sin'] = np.sin(2 * np.pi * d['month'] / 12)
    d['month_cos'] = np.cos(2 * np.pi * d['month'] / 12)
    d['dow_sin'] = np.sin(2 * np.pi * d['day_of_week'] / 7)
    d['dow_cos'] = np.cos(2 * np.pi * d['day_of_week'] / 7)
    d['doy_sin'] = np.sin(2 * np.pi * d['day_of_year'] / 365.25)
    d['doy_cos'] = np.cos(2 * np.pi * d['day_of_year'] / 365.25)
    
    # Seasonal patterns for Tirupati
    season_map = {1:0, 2:0, 3:1, 4:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:3, 11:3, 12:0}
    d['season'] = d['month'].map(season_map)
    
    # Climate indicators
    d['is_sw_monsoon'] = d['month'].isin([6, 7, 8, 9]).astype(int)
    d['is_ne_monsoon'] = d['month'].isin([10, 11]).astype(int)
    d['is_summer'] = d['month'].isin([3, 4, 5]).astype(int)
    d['is_winter'] = d['month'].isin([12, 1, 2]).astype(int)
    
    # Time of day indicators
    d['is_daytime'] = ((d['hour'] >= 6) & (d['hour'] <= 18)).astype(int)
    d['is_peak_solar'] = ((d['hour'] >= 10) & (d['hour'] <= 14)).astype(int)
    d['is_night'] = ((d['hour'] >= 20) | (d['hour'] <= 5)).astype(int)
    d['is_morning'] = ((d['hour'] >= 5) & (d['hour'] <= 9)).astype(int)
    d['is_evening'] = ((d['hour'] >= 16) & (d['hour'] <= 20)).astype(int)
    
    # Long-term trend
    d['year_trend'] = (d['year'] - 2015) / 10.0
    
    return d

def get_optimized_xgb_params(target):
    """Get optimized XGBoost hyperparameters for different targets"""
    base_params = {
        'learning_rate': 0.05,
        'subsample': 0.9,
        'colsample_bytree': 0.85,
        'random_state': 42,
        'n_jobs': -1,
        'verbosity': 0
    }
    
    # Target-specific optimizations
    if target == 'PRECTOTCORR':
        return {**base_params, 'n_estimators': 250, 'max_depth': 8, 'min_child_weight': 3, 'gamma': 0.5}
    elif target in ['T2M', 'T2MDEW', 'T2MWET']:
        return {**base_params, 'n_estimators': 200, 'max_depth': 7, 'min_child_weight': 2, 'gamma': 0.1}
    elif target in ['RH2M', 'QV2M']:
        return {**base_params, 'n_estimators': 180, 'max_depth': 7, 'min_child_weight': 2, 'gamma': 0.2}
    elif target in ['WS10M', 'WS50M']:
        return {**base_params, 'n_estimators': 200, 'max_depth': 8, 'min_child_weight': 2, 'gamma': 0.3}
    else:
        return {**base_params, 'n_estimators': 180, 'max_depth': 7, 'min_child_weight': 2, 'gamma': 0.1}

def train_optimized_model(X_train, X_test, y_train, y_test, target):
    """Train model with hyperparameter optimization"""
    if target in ['WD10M', 'WD50M']:
        # Use RandomSearch for wind direction
        model = RandomForestRegressor(random_state=42, n_jobs=-1)
        param_dist = {
            'n_estimators': [150, 200, 250, 300],
            'max_depth': [8, 10, 12, 15, 18],
            'min_samples_split': [2, 5, 8],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2']
        }
        search = RandomizedSearchCV(model, param_dist, n_iter=15, cv=3, scoring='r2', 
                                   n_jobs=-1, random_state=42, verbose=0)
        search.fit(X_train, y_train)
        return search.best_estimator_
    else:
        # XGBoost with optimized parameters
        params = get_optimized_xgb_params(target)
        model = xgb.XGBRegressor(**params)
        
        # Fit the model using local dataset features. XGBoost 3.x removed sklearn-style early stopping arguments.
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        return model

def main():
    print("🌤️ MBU Weather Intelligence - Training Models with Hyperparameter Tuning")
    print("=" * 75)
    
    # Load data
    print("📊 Loading dataset...")
    df = pd.read_csv('data.csv')
    df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%Y-%m-%d-%H')
    df = df.sort_values('DATETIME').reset_index(drop=True)
    
    print(f"✅ Loaded {len(df):,} records from {df['DATETIME'].min()} to {df['DATETIME'].max()}")
    
    # Create features
    print("🔧 Creating time-based features...")
    df_features = create_time_features(df)
    
    # Define features and targets
    TIME_FEATURES = [
        'year', 'month', 'day', 'hour', 'day_of_year', 'day_of_week',
        'week_of_year', 'quarter', 'hour_sin', 'hour_cos', 'month_sin',
        'month_cos', 'dow_sin', 'dow_cos', 'doy_sin', 'doy_cos', 'season',
        'is_sw_monsoon', 'is_ne_monsoon', 'is_summer', 'is_winter',
        'is_daytime', 'is_peak_solar', 'is_night', 'is_morning', 'is_evening',
        'year_trend'
    ]
    
    WEATHER_TARGETS = [
        'PS', 'WS10M', 'WD10M', 'WS50M', 'WD50M', 'QV2M', 'RH2M',
        'PRECTOTCORR', 'T2MWET', 'T2MDEW', 'T2M', 'ALLSKY_SFC_SW_DWN',
        'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DNI', 'ALLSKY_SFC_SW_DIFF',
        'ALLSKY_KT', 'ALLSKY_SRF_ALB', 'SZA', 'ALLSKY_SFC_PAR_TOT',
        'CLRSKY_SFC_PAR_TOT', 'ALLSKY_SFC_UVA', 'ALLSKY_SFC_UVB',
        'ALLSKY_SFC_UV_INDEX'
    ]
    
    X = df_features[TIME_FEATURES]
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    print(f"🤖 Training {len(WEATHER_TARGETS)} optimized weather prediction models...")
    print(f"⏱️  Hyperparameter tuning may take 10-20 minutes. Please wait...\n")
    
    models = {}
    scalers = {}
    results = {}
    
    for i, target in enumerate(WEATHER_TARGETS, 1):
        print(f"[{i:2d}/{len(WEATHER_TARGETS)}] {target:<25}", end=" ", flush=True)
        
        y = df_features[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train with optimization
        model = train_optimized_model(X_train_scaled, X_test_scaled, y_train, y_test, target)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Store results
        models[target] = model
        scalers[target] = scaler
        results[target] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        
        # Save immediately
        joblib.dump(model, f'models/{target}_model.pkl')
        joblib.dump(scaler, f'models/{target}_scaler.pkl')
        
        print(f"✅ MAE: {mae:8.4f}  RMSE: {rmse:8.4f}  R²: {r2:7.4f}")
    
    print(f"\n🌧️ Training rainfall classifier with optimization...")
    
    # Rainfall classifier
    rain_threshold = 0.1
    y_rain = (df_features['PRECTOTCORR'] > rain_threshold).astype(int)
    
    X_train, X_test, y_train_rain, y_test_rain = train_test_split(
        X, y_rain, test_size=0.2, random_state=42, shuffle=False
    )
    
    scaler_rain = StandardScaler()
    X_train_scaled = scaler_rain.fit_transform(X_train)
    X_test_scaled = scaler_rain.transform(X_test)
    
    # Optimized rainfall classifier
    rain_model = RandomForestClassifier(
        n_estimators=200, max_depth=12, min_samples_split=5,
        random_state=42, class_weight='balanced', n_jobs=-1
    )
    rain_model.fit(X_train_scaled, y_train_rain)
    
    y_pred_rain = rain_model.predict(X_test_scaled)
    rain_accuracy = accuracy_score(y_test_rain, y_pred_rain)
    
    joblib.dump(rain_model, 'models/RAIN_classifier.pkl')
    joblib.dump(scaler_rain, 'models/RAIN_scaler.pkl')
    
    print(f"✅ Rainfall Classifier Accuracy: {rain_accuracy:.4f}\n")
    
    # Save metadata
    print(f"💾 Saving metadata...")
    
    WEATHER_METADATA = {
        'PS': {'name': 'Surface Pressure', 'unit': 'kPa', 'icon': '🌍', 'min_val': 95.0, 'max_val': 105.0, 'decimals': 2},
        'WS10M': {'name': 'Wind Speed (10m)', 'unit': 'm/s', 'icon': '🌬️', 'min_val': 0.0, 'max_val': 20.0, 'decimals': 2},
        'WD10M': {'name': 'Wind Direction (10m)', 'unit': '°', 'icon': '🧭', 'min_val': 0.0, 'max_val': 360.0, 'decimals': 1},
        'WS50M': {'name': 'Wind Speed (50m)', 'unit': 'm/s', 'icon': '🌬️', 'min_val': 0.0, 'max_val': 25.0, 'decimals': 2},
        'WD50M': {'name': 'Wind Direction (50m)', 'unit': '°', 'icon': '🧭', 'min_val': 0.0, 'max_val': 360.0, 'decimals': 1},
        'QV2M': {'name': 'Specific Humidity', 'unit': 'g/kg', 'icon': '💧', 'min_val': 0.0, 'max_val': 30.0, 'decimals': 2},
        'RH2M': {'name': 'Relative Humidity', 'unit': '%', 'icon': '💦', 'min_val': 0.0, 'max_val': 100.0, 'decimals': 1},
        'PRECTOTCORR': {'name': 'Rainfall', 'unit': 'mm/hr', 'icon': '🌧️', 'min_val': 0.0, 'max_val': 50.0, 'decimals': 2},
        'T2MWET': {'name': 'Wet Bulb Temperature', 'unit': '°C', 'icon': '🌡️', 'min_val': 5.0, 'max_val': 40.0, 'decimals': 2},
        'T2MDEW': {'name': 'Dew Point', 'unit': '°C', 'icon': '🌫️', 'min_val': 0.0, 'max_val': 35.0, 'decimals': 2},
        'T2M': {'name': 'Air Temperature', 'unit': '°C', 'icon': '🌡️', 'min_val': 10.0, 'max_val': 50.0, 'decimals': 2},
        'ALLSKY_SFC_SW_DWN': {'name': 'Solar Irradiance', 'unit': 'Wh/m²', 'icon': '☀️', 'min_val': 0.0, 'max_val': 1000.0, 'decimals': 0},
        'CLRSKY_SFC_SW_DWN': {'name': 'Clear Sky Solar', 'unit': 'Wh/m²', 'icon': '🌤️', 'min_val': 0.0, 'max_val': 1000.0, 'decimals': 0},
        'ALLSKY_SFC_SW_DNI': {'name': 'Direct Solar', 'unit': 'Wh/m²', 'icon': '☀️', 'min_val': 0.0, 'max_val': 1000.0, 'decimals': 0},
        'ALLSKY_SFC_SW_DIFF': {'name': 'Diffuse Solar', 'unit': 'Wh/m²', 'icon': '🌫️', 'min_val': 0.0, 'max_val': 500.0, 'decimals': 0},
        'ALLSKY_KT': {'name': 'Clearness Index', 'unit': '', 'icon': '📊', 'min_val': 0.0, 'max_val': 1.0, 'decimals': 3},
        'ALLSKY_SRF_ALB': {'name': 'Surface Albedo', 'unit': '', 'icon': '🪞', 'min_val': 0.0, 'max_val': 1.0, 'decimals': 3},
        'SZA': {'name': 'Solar Zenith Angle', 'unit': '°', 'icon': '📐', 'min_val': 0.0, 'max_val': 90.0, 'decimals': 1},
        'ALLSKY_SFC_PAR_TOT': {'name': 'PAR Total', 'unit': 'W/m²', 'icon': '🌱', 'min_val': 0.0, 'max_val': 500.0, 'decimals': 1},
        'CLRSKY_SFC_PAR_TOT': {'name': 'PAR Clear Sky', 'unit': 'W/m²', 'icon': '🌱', 'min_val': 0.0, 'max_val': 500.0, 'decimals': 1},
        'ALLSKY_SFC_UVA': {'name': 'UVA Radiation', 'unit': 'Wh/m²', 'icon': '🕶️', 'min_val': 0.0, 'max_val': 10.0, 'decimals': 2},
        'ALLSKY_SFC_UVB': {'name': 'UVB Radiation', 'unit': 'Wh/m²', 'icon': '🕶️', 'min_val': 0.0, 'max_val': 5.0, 'decimals': 3},
        'ALLSKY_SFC_UV_INDEX': {'name': 'UV Index', 'unit': '', 'icon': '🌞', 'min_val': 0.0, 'max_val': 15.0, 'decimals': 1}
    }
    
    joblib.dump(TIME_FEATURES, 'models/feature_names.pkl')
    joblib.dump(WEATHER_METADATA, 'models/weather_metadata.pkl')
    joblib.dump(WEATHER_TARGETS, 'models/weather_targets.pkl')
    joblib.dump(results, 'models/model_results.pkl')
    
    print(f"✅ Saved all metadata files\n")
    
    # Print results summary
    print("📊 MODEL PERFORMANCE SUMMARY")
    print("=" * 75)
    avg_r2 = np.mean([results[t]['R2'] for t in WEATHER_TARGETS])
    print(f"Average R² Score: {avg_r2:.4f}")
    print(f"Best R² Score: {max([results[t]['R2'] for t in WEATHER_TARGETS]):.4f} ({max(results, key=lambda x: results[x]['R2'])})")
    print(f"Worst R² Score: {min([results[t]['R2'] for t in WEATHER_TARGETS]):.4f} ({min(results, key=lambda x: results[x]['R2'])})")
    
    # Test prediction
    print(f"\n🔮 Testing prediction...")
    test_dt = datetime(2026, 7, 15, 14, 0, 0)
    test_data = pd.DataFrame([{'DATETIME': test_dt}])
    test_features = create_time_features(test_data)
    X_test = test_features[TIME_FEATURES]
    
    print(f"Sample predictions for {test_dt.strftime('%B %d, %Y at %I:%M %p')}:")
    for target in ['T2M', 'RH2M', 'PRECTOTCORR', 'WS10M']:
        X_scaled = scalers[target].transform(X_test)
        pred = models[target].predict(X_scaled)[0]
        meta = WEATHER_METADATA[target]
        print(f"  {meta['icon']} {meta['name']}: {pred:.2f} {meta['unit']}")
    
    print(f"\n🎉 TRAINING COMPLETE!")
    print(f"✅ Trained {len(WEATHER_TARGETS)} optimized weather models")
    print(f"✅ Created optimized rainfall classifier")
    print(f"✅ Saved all models to 'models/' directory")
    print(f"🚀 Ready to run: streamlit run app.py")

    # Optional: Deep Learning LSTM for temperature (improves temporal consistency)
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from tensorflow.keras.callbacks import EarlyStopping
        print("\n🤖 TensorFlow detected — training optional LSTM for `T2M` to improve temporal accuracy...")

        def create_sequences(X_arr, y_arr, lookback=24):
            Xs, ys = [], []
            for i in range(len(X_arr) - lookback):
                Xs.append(X_arr[i:(i+lookback)])
                ys.append(y_arr[i+lookback])
            return np.array(Xs), np.array(ys)

        lookback = 24
        target_dl = 'T2M'

        X_full = df_features[TIME_FEATURES].values
        y_full = df_features[target_dl].values

        # scale X and y
        scaler_X_dl = StandardScaler()
        X_scaled_full = scaler_X_dl.fit_transform(X_full)
        scaler_y_dl = StandardScaler()
        y_scaled_full = scaler_y_dl.fit_transform(y_full.reshape(-1,1)).ravel()

        X_seq, y_seq = create_sequences(X_scaled_full, y_scaled_full, lookback=lookback)

        # train/test split (temporal)
        split_idx = int(0.8 * len(X_seq))
        X_train_dl, X_test_dl = X_seq[:split_idx], X_seq[split_idx:]
        y_train_dl, y_test_dl = y_seq[:split_idx], y_seq[split_idx:]

        # build model
        model_dl = Sequential([
            LSTM(64, input_shape=(X_train_dl.shape[1], X_train_dl.shape[2]), return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1)
        ])

        model_dl.compile(optimizer='adam', loss='mse', metrics=['mae'])

        es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        model_dl.fit(
            X_train_dl, y_train_dl,
            validation_data=(X_test_dl, y_test_dl),
            epochs=20, batch_size=32, callbacks=[es], verbose=1
        )

        # Evaluate and save
        dl_preds = model_dl.predict(X_test_dl).ravel()
        dl_preds_inv = scaler_y_dl.inverse_transform(dl_preds.reshape(-1,1)).ravel()
        y_test_inv = scaler_y_dl.inverse_transform(y_test_dl.reshape(-1,1)).ravel()

        dl_mae = mean_absolute_error(y_test_inv, dl_preds_inv)
        dl_rmse = np.sqrt(mean_squared_error(y_test_inv, dl_preds_inv))
        dl_r2 = r2_score(y_test_inv, dl_preds_inv)

        print(f"\n🔬 LSTM Results for {target_dl} — MAE: {dl_mae:.4f}, RMSE: {dl_rmse:.4f}, R²: {dl_r2:.4f}")

        # Save model and scalers
        model_dl.save('models/T2M_lstm')
        joblib.dump(scaler_X_dl, 'models/T2M_lstm_X_scaler.pkl')
        joblib.dump(scaler_y_dl, 'models/T2M_lstm_y_scaler.pkl')
        print("💾 Saved LSTM model to models/T2M_lstm/")

    except Exception as e:
        print("\n⚠️ TensorFlow not available or error during DL training — skipping LSTM block.")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()
