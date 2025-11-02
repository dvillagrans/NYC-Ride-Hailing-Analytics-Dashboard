#!/usr/bin/env python3
"""
Script para entrenar modelos de machine learning para el dashboard de NYC Ride-Hailing Analytics.

Este script entrena múltiples modelos:
1. Predicción de tarifas (driver_pay)
2. Clasificación de viajes a aeropuertos
3. Predicción de duración de viajes

Utiliza tanto algoritmos tradicionales (RandomForest, XGBoost) como redes neuronales (TensorFlow).
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importaciones para modelos tradicionales
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import lightgbm as lgb

# Importaciones para TensorFlow (opcional)
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    HAS_TENSORFLOW = True
    print("✅ TensorFlow disponible - Se entrenarán modelos de redes neuronales")
except ImportError:
    HAS_TENSORFLOW = False
    print("⚠️ TensorFlow no disponible - Solo se entrenarán modelos tradicionales")

# Configuración
MODEL_DIR = 'models'
DATA_FOLDER = 'data'
SAMPLE_SIZE = 50000  # Muestra para entrenamiento rápido

def setup_directories():
    """Crear directorios necesarios."""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"✅ Creado directorio: {MODEL_DIR}")

def load_data():
    """Cargar y preparar los datos para entrenamiento."""
    print("📊 Cargando datos...")
    
    # Buscar archivos de datos
    import glob
    data_files = glob.glob(f"{DATA_FOLDER}/*_reduced.parquet")
    
    if not data_files:
        print("❌ No se encontraron archivos de datos. Ejecuta extract_data.py primero.")
        sys.exit(1)
    
    # Cargar todos los archivos
    dfs = []
    for file in data_files:
        df = pd.read_parquet(file)
        dfs.append(df)
        print(f"   Cargado: {file} ({len(df):,} registros)")
    
    # Combinar datos
    df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Datos combinados: {len(df):,} registros totales")
    
    # Tomar muestra para entrenamiento más rápido
    if len(df) > SAMPLE_SIZE:
        df = df.sample(n=SAMPLE_SIZE, random_state=42)
        print(f"📝 Usando muestra de {SAMPLE_SIZE:,} registros para entrenamiento")
    
    return df

def prepare_features(df):
    """Preparar características para los modelos."""
    print("🔧 Preparando características...")
    
    # Crear características temporales
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['month'] = df['pickup_datetime'].dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Calcular duración del viaje en minutos
    df['trip_time_minutes'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    
    # Características básicas para modelos
    feature_columns = [
        'trip_miles', 'trip_time_minutes', 'hour', 'day_of_week', 
        'month', 'is_weekend', 'PULocationID', 'DOLocationID'
    ]
    
    # Limpiar datos
    df = df.dropna(subset=feature_columns + ['driver_pay'])
    df = df[df['trip_miles'] > 0]
    df = df[df['trip_time_minutes'] > 0]
    df = df[df['driver_pay'] > 0]
    
    print(f"✅ Datos limpios: {len(df):,} registros")
    return df, feature_columns

def create_airport_labels(df):
    """Crear etiquetas para clasificación de aeropuertos."""
    # IDs de zonas de aeropuertos en NYC
    airport_zones = [1, 132, 138, 161, 162, 163]  # JFK, LGA, EWR principales
    
    df['to_airport'] = df['DOLocationID'].isin(airport_zones).astype(int)
    df['from_airport'] = df['PULocationID'].isin(airport_zones).astype(int)
    df['airport_trip'] = ((df['to_airport'] == 1) | (df['from_airport'] == 1)).astype(int)
    
    return df

def train_fare_prediction_models(df, features):
    """Entrenar modelos de predicción de tarifas."""
    print("\n💰 Entrenando modelos de predicción de tarifas...")
    
    X = df[features]
    y = df['driver_pay']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {}
    
    # 1. Random Forest
    print("   🌳 Entrenando Random Forest...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    models['driver_pay_rf'] = {
        'model': rf_model,
        'metrics': {'rmse': rmse, 'r2': r2},
        'type': 'traditional'
    }
    print(f"      RMSE: {rmse:.4f}, R²: {r2:.4f}")
    
    # 2. LightGBM
    print("   🚀 Entrenando LightGBM...")
    lgb_model = lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
    lgb_model.fit(X_train, y_train)
    
    y_pred = lgb_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    models['driver_pay_lgb'] = {
        'model': lgb_model,
        'metrics': {'rmse': rmse, 'r2': r2},
        'type': 'traditional'
    }
    print(f"      RMSE: {rmse:.4f}, R²: {r2:.4f}")
    
    # 3. Red Neuronal (si TensorFlow está disponible)
    if HAS_TENSORFLOW:
        print("   🧠 Entrenando Red Neuronal...")
        
        # Normalizar datos
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Crear modelo
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # Entrenar
        history = model.fit(
            X_train_scaled, y_train,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        # Evaluar
        y_pred = model.predict(X_test_scaled, verbose=0).flatten()
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        models['driver_pay_nn'] = {
            'model': model,
            'scaler': scaler,
            'metrics': {'rmse': rmse, 'r2': r2},
            'type': 'neural_network'
        }
        print(f"      RMSE: {rmse:.4f}, R²: {r2:.4f}")
    
    return models

def train_airport_classification_models(df, features):
    """Entrenar modelos de clasificación de aeropuertos."""
    print("\n✈️ Entrenando modelos de clasificación de aeropuertos...")
    
    df = create_airport_labels(df)
    
    X = df[features]
    y = df['airport_trip']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {}
    
    # 1. Random Forest
    print("   🌳 Entrenando Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    models['airport_rf'] = {
        'model': rf_model,
        'metrics': {'accuracy': accuracy},
        'type': 'traditional'
    }
    print(f"      Precisión: {accuracy:.4f}")
    
    # 2. LightGBM
    print("   🚀 Entrenando LightGBM...")
    lgb_model = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    lgb_model.fit(X_train, y_train)
    
    y_pred = lgb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    models['airport_lgb'] = {
        'model': lgb_model,
        'metrics': {'accuracy': accuracy},
        'type': 'traditional'
    }
    print(f"      Precisión: {accuracy:.4f}")
    
    return models

def save_models(models):
    """Guardar modelos entrenados."""
    print("\n💾 Guardando modelos...")
    
    for name, model_data in models.items():
        metrics_path = os.path.join(MODEL_DIR, f"{name}_metrics.json")
        
        if model_data['type'] == 'traditional':
            # Guardar modelo tradicional
            model_path = os.path.join(MODEL_DIR, f"{name}.joblib")
            joblib.dump(model_data['model'], model_path)
            print(f"   ✅ {name}: {model_path}")
            
        elif model_data['type'] == 'neural_network':
            # Guardar red neuronal con extensión .keras
            nn_path = os.path.join(MODEL_DIR, f"{name}_nn.keras")
            model_data['model'].save(nn_path)
            
            # Guardar scaler por separado
            scaler_path = os.path.join(MODEL_DIR, f"{name}_scaler.joblib")
            joblib.dump(model_data['scaler'], scaler_path)
            print(f"   ✅ {name}: {nn_path}")
        
        # Guardar métricas
        with open(metrics_path, 'w') as f:
            json.dump(model_data['metrics'], f, indent=2)

def main():
    """Función principal."""
    print("🚀 Iniciando entrenamiento de modelos ML para NYC Ride-Hailing Analytics")
    print("=" * 70)
    
    # Configurar directorios
    setup_directories()
    
    # Cargar datos
    df = load_data()
    
    # Preparar características
    df, features = prepare_features(df)
    
    # Entrenar modelos
    all_models = {}
    
    # Modelos de predicción de tarifas
    fare_models = train_fare_prediction_models(df, features)
    all_models.update(fare_models)
    
    # Modelos de clasificación de aeropuertos
    airport_models = train_airport_classification_models(df, features)
    all_models.update(airport_models)
    
    # Guardar modelos
    save_models(all_models)
    
    print("\n" + "=" * 70)
    print("🎉 ¡Entrenamiento completado exitosamente!")
    print(f"📁 Modelos guardados en: {MODEL_DIR}/")
    print(f"🔢 Total de modelos entrenados: {len(all_models)}")
    print("\n💡 Ahora puedes usar los modelos en el dashboard:")
    print("   streamlit run app.py")
    print("   Navega a la pestaña 'Modelos ML' para probar las predicciones")

if __name__ == "__main__":
    main()