# 📋 Documentación Técnica

> **Arquitectura, diseño y especificaciones técnicas del NYC Ride-Hailing Analytics Dashboard**

## 📋 Tabla de Contenidos

- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura de Datos](#-estructura-de-datos)
- [Modelos de Machine Learning](#-modelos-de-machine-learning)
- [API y Funciones](#-api-y-funciones)
- [Optimizaciones de Rendimiento](#-optimizaciones-de-rendimiento)
- [Seguridad y Mejores Prácticas](#-seguridad-y-mejores-prácticas)
- [Escalabilidad](#-escalabilidad)

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```mermaid
graph TD
    A[Usuario] --> B[Streamlit Frontend]
    B --> C[Data Processing Layer]
    C --> D[Pandas/NumPy]
    C --> E[Model Utils]
    E --> F[ML Models]
    F --> G[Scikit-learn]
    F --> H[TensorFlow/Keras]
    C --> I[Visualization Layer]
    I --> J[Plotly]
    I --> K[Folium]
    I --> L[PyDeck]
    C --> M[Data Storage]
    M --> N[Parquet Files]
    M --> O[CSV Files]
    M --> P[Joblib Models]
```

### Componentes Principales

#### 1. **Frontend Layer (Streamlit)**
- **Responsabilidad**: Interfaz de usuario y presentación
- **Tecnologías**: Streamlit, HTML/CSS personalizado
- **Características**:
  - Interfaz reactiva y responsiva
  - Navegación por pestañas
  - Filtros dinámicos en sidebar
  - Caching automático de datos

#### 2. **Data Processing Layer**
- **Responsabilidad**: Procesamiento y transformación de datos
- **Tecnologías**: Pandas, NumPy, PyArrow
- **Funciones**:
  - Carga de datos desde Parquet
  - Filtrado y agregación
  - Transformaciones temporales
  - Joins con datos de referencia

#### 3. **Machine Learning Layer**
- **Responsabilidad**: Predicciones y clasificaciones
- **Tecnologías**: Scikit-learn, TensorFlow, XGBoost, LightGBM
- **Modelos**:
  - Regresión para predicción de tarifas
  - Clasificación para viajes a aeropuertos
  - Análisis de importancia de características

#### 4. **Visualization Layer**
- **Responsabilidad**: Generación de gráficos y mapas
- **Tecnologías**: Plotly, Folium, PyDeck, Matplotlib
- **Tipos de visualización**:
  - Gráficos interactivos (Plotly)
  - Mapas 2D (Folium)
  - Visualizaciones 3D (PyDeck)
  - Mapas de calor

#### 5. **Data Storage Layer**
- **Responsabilidad**: Almacenamiento y persistencia
- **Formatos**: Parquet (datos), CSV (referencia), Joblib (modelos)
- **Estructura optimizada para consultas analíticas**

## 🛠️ Stack Tecnológico

### Core Technologies

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|----------|
| **Frontend** | Streamlit | 1.28+ | Dashboard interactivo |
| **Data Processing** | Pandas | 2.0+ | Manipulación de datos |
| **Numerical Computing** | NumPy | 1.24+ | Operaciones numéricas |
| **Visualization** | Plotly | 5.15+ | Gráficos interactivos |
| **Geospatial** | Folium | 0.14+ | Mapas 2D |
| **3D Visualization** | PyDeck | 0.8+ | Visualizaciones 3D |
| **ML Framework** | Scikit-learn | 1.3+ | Modelos tradicionales |
| **Deep Learning** | TensorFlow | 2.13+ | Redes neuronales |
| **Data Format** | PyArrow | 12.0+ | Parquet I/O |

### Dependencias Especializadas

```python
# Análisis de datos
import pandas as pd
import numpy as np
import pyarrow.parquet as pq

# Visualización
import plotly.express as px
import plotly.graph_objects as go
import folium
import pydeck as pdk

# Machine Learning
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import xgboost as xgb

# Deep Learning (opcional)
import tensorflow as tf
from tensorflow import keras

# Utilidades
import joblib
import datetime
import glob
import os
```

## 📊 Estructura de Datos

### Schema Principal

```python
# Esquema de datos de viajes
TRIP_SCHEMA = {
    'pickup_datetime': 'datetime64[ns]',
    'dropoff_datetime': 'datetime64[ns]',
    'hvfhs_license_num': 'object',  # Uber, Lyft, etc.
    'PULocationID': 'int64',        # Zona de recogida
    'DOLocationID': 'int64',        # Zona de destino
    'trip_miles': 'float64',        # Distancia en millas
    'trip_time': 'int64',           # Duración en segundos
    'base_passenger_fare': 'float64',
    'tolls': 'float64',
    'bcf': 'float64',               # Black Car Fund
    'sales_tax': 'float64',
    'congestion_surcharge': 'float64',
    'airport_fee': 'float64',
    'tips': 'float64',
    'driver_pay': 'float64',        # Variable objetivo principal
    'shared_request_flag': 'object',
    'shared_match_flag': 'object',
    'access_a_ride_flag': 'object', # Servicios de accesibilidad
    'wav_request_flag': 'object',   # Wheelchair accessible
    'wav_match_flag': 'object'
}
```

### Datos de Referencia

```python
# Zonas de NYC
ZONE_SCHEMA = {
    'LocationID': 'int64',
    'Borough': 'object',
    'Zone': 'object',
    'service_zone': 'object'
}

# Centroides de zonas
CENTROID_SCHEMA = {
    'LocationID': 'int64',
    'latitude': 'float64',
    'longitude': 'float64'
}
```

### Transformaciones de Datos

```python
def preprocess_data(df):
    """
    Aplica transformaciones estándar a los datos de viajes.
    """
    # Conversión de tipos
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    
    # Características temporales
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_weekday'] = df['pickup_datetime'].dt.weekday
    df['pickup_month'] = df['pickup_datetime'].dt.month
    
    # Mapeo de días
    days_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 
                3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    df['day_name'] = df['pickup_weekday'].map(days_map)
    
    # Identificación de aeropuertos
    airport_zones = [1, 132, 138]  # Newark, JFK, LaGuardia
    df['from_airport'] = df['PULocationID'].isin(airport_zones)
    df['to_airport'] = df['DOLocationID'].isin(airport_zones)
    
    # Limpieza de datos
    df = df.dropna(subset=['driver_pay', 'trip_miles', 'trip_time'])
    df = df[df['driver_pay'] > 0]
    df = df[df['trip_miles'] > 0]
    
    return df
```

## 🤖 Modelos de Machine Learning

### Arquitectura de Modelos

```mermaid
graph LR
    A[Raw Data] --> B[Preprocessing]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[Model Validation]
    E --> F[Model Persistence]
    F --> G[Prediction API]
```

### 1. Predictor de Tarifas

```python
class FarePredictor:
    """
    Modelo para predecir el costo de viajes (driver_pay).
    """
    
    def __init__(self):
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42
            ))
        ])
    
    def get_features(self):
        return [
            'trip_miles', 'trip_time', 'pickup_hour',
            'pickup_weekday', 'base_passenger_fare',
            'tolls', 'airport_fee', 'to_airport', 'from_airport'
        ]
    
    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        return self.model.predict(X)
```

### 2. Clasificador de Aeropuertos

```python
class AirportClassifier:
    """
    Modelo para clasificar viajes hacia/desde aeropuertos.
    """
    
    def __init__(self):
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                class_weight='balanced',
                random_state=42
            ))
        ])
    
    def get_features(self):
        return [
            'trip_miles', 'trip_time', 'pickup_hour',
            'pickup_weekday', 'base_passenger_fare'
        ]
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]
```

### 3. Red Neuronal (TensorFlow)

```python
def create_neural_network(input_dim):
    """
    Crea una red neuronal para predicción de tarifas.
    """
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='linear')
    ])
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model
```

## 🔧 API y Funciones

### Core Functions

```python
# model_utils.py - API principal

def get_available_models():
    """
    Retorna información de modelos disponibles.
    """
    pass

def load_model(model_name):
    """
    Carga un modelo entrenado desde disco.
    """
    pass

def predict_fare(df, features=None):
    """
    Predice tarifas para un DataFrame de viajes.
    """
    pass

def predict_airport(df, features=None):
    """
    Clasifica viajes como aeroportuarios o no.
    """
    pass

def get_feature_importance(model_name):
    """
    Retorna importancia de características del modelo.
    """
    pass
```

### Streamlit Components

```python
# Componentes reutilizables

@st.cache_data
def load_data(file_path):
    """
    Carga datos con caching automático.
    """
    return pd.read_parquet(file_path)

@st.cache_resource
def load_ml_model(model_name):
    """
    Carga modelo ML con caching de recursos.
    """
    return joblib.load(f'models/{model_name}.joblib')

def create_metric_card(title, value, delta=None):
    """
    Crea tarjeta de métrica estilizada.
    """
    st.metric(label=title, value=value, delta=delta)

def create_plotly_chart(fig, title=None):
    """
    Renderiza gráfico Plotly con configuración estándar.
    """
    if title:
        fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)
```

## ⚡ Optimizaciones de Rendimiento

### 1. Caching Strategy

```python
# Streamlit caching
@st.cache_data(ttl=3600)  # Cache por 1 hora
def expensive_computation(data):
    # Operación costosa
    return result

@st.cache_resource  # Cache persistente
def load_large_model():
    return joblib.load('large_model.joblib')
```

### 2. Data Loading Optimization

```python
# Carga optimizada de Parquet
def load_parquet_optimized(file_path, columns=None):
    """
    Carga solo columnas necesarias para reducir memoria.
    """
    return pd.read_parquet(file_path, columns=columns)

# Filtrado temprano
def filter_data_early(df, filters):
    """
    Aplica filtros antes de operaciones costosas.
    """
    for column, values in filters.items():
        if column in df.columns:
            df = df[df[column].isin(values)]
    return df
```

### 3. Memory Management

```python
# Gestión de memoria
def optimize_dtypes(df):
    """
    Optimiza tipos de datos para reducir uso de memoria.
    """
    # Convertir a categorías
    categorical_cols = ['hvfhs_license_num', 'pickup_borough']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    
    # Downcast numéricos
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    return df
```

### 4. Parallel Processing

```python
# Procesamiento paralelo para entrenamiento
from joblib import Parallel, delayed

def train_models_parallel(data_chunks):
    """
    Entrena múltiples modelos en paralelo.
    """
    results = Parallel(n_jobs=-1)(
        delayed(train_single_model)(chunk) 
        for chunk in data_chunks
    )
    return results
```

## 🔒 Seguridad y Mejores Prácticas

### 1. Data Validation

```python
from pydantic import BaseModel, validator

class TripData(BaseModel):
    trip_miles: float
    trip_time: int
    pickup_hour: int
    driver_pay: float
    
    @validator('trip_miles')
    def validate_miles(cls, v):
        if v <= 0 or v > 1000:
            raise ValueError('Invalid trip distance')
        return v
    
    @validator('pickup_hour')
    def validate_hour(cls, v):
        if v < 0 or v > 23:
            raise ValueError('Invalid hour')
        return v
```

### 2. Error Handling

```python
def safe_model_prediction(model, data):
    """
    Predicción con manejo seguro de errores.
    """
    try:
        return model.predict(data)
    except Exception as e:
        st.error(f"Error en predicción: {str(e)}")
        return None
```

### 3. Input Sanitization

```python
def sanitize_user_input(value, data_type, min_val=None, max_val=None):
    """
    Sanitiza entrada del usuario.
    """
    try:
        value = data_type(value)
        if min_val is not None and value < min_val:
            return min_val
        if max_val is not None and value > max_val:
            return max_val
        return value
    except (ValueError, TypeError):
        return None
```

## 📈 Escalabilidad

### 1. Horizontal Scaling

```python
# Configuración para múltiples workers
# streamlit_config.toml
[server]
maxUploadSize = 1000
enableCORS = false
enableXsrfProtection = true

[browser]
serverAddress = "0.0.0.0"
serverPort = 8501
```

### 2. Database Integration

```python
# Conexión a base de datos (futuro)
import sqlalchemy as sa

def create_db_connection():
    engine = sa.create_engine(
        'postgresql://user:pass@localhost/nyc_trips'
    )
    return engine

def load_data_from_db(query, params=None):
    engine = create_db_connection()
    return pd.read_sql(query, engine, params=params)
```

### 3. Microservices Architecture

```python
# API separada para modelos ML
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict/fare")
async def predict_fare_api(trip_data: TripData):
    prediction = model.predict([trip_data.dict()])
    return {"predicted_fare": float(prediction[0])}
```

### 4. Monitoring y Logging

```python
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_user_action(action, details):
    logger.info(f"User action: {action}, Details: {details}")
```

## 🔄 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboard

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Streamlit Cloud
      run: echo "Deploying to production"
```

---

<div align="center">
  <strong>📋 Documentación técnica completa para desarrollo y mantenimiento 📋</strong>
</div>