import os
import joblib
import pandas as pd
import numpy as np
try:
    import tensorflow as tf
    from tensorflow import keras
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    print("TensorFlow no está disponible. Se usarán solo modelos tradicionales.")

# Directorio para modelos
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

def get_available_models():
    """
    Obtiene la lista de modelos disponibles en el directorio de modelos.
    
    Returns:
        dict: Diccionario con información de los modelos disponibles
    """
    if not os.path.exists(MODEL_DIR):
        return {}
    
    models = {}
    
    # Buscar modelos tradicionales (.joblib)
    joblib_models = [f for f in os.listdir(MODEL_DIR) if f.endswith('.joblib') and '_metrics' not in f and '_scaler' not in f]
    
    for model_file in joblib_models:
        model_name = model_file.replace('.joblib', '')
        metrics_file = f"{model_name}_metrics.json"
        
        if os.path.exists(os.path.join(MODEL_DIR, metrics_file)):
            import json
            with open(os.path.join(MODEL_DIR, metrics_file), 'r') as f:
                metrics = json.load(f)
            models[model_name] = {
                'type': 'joblib',
                'file': model_file,
                'metrics': metrics
            }
    
    # Buscar modelos de redes neuronales (.keras)
    keras_models = [f for f in os.listdir(MODEL_DIR) if f.endswith('.keras')]
    
    for model_file in keras_models:
        model_name = model_file.replace('.keras', '').replace('_nn', '')
        metrics_file = f"{model_name}_nn_metrics.json"
        scaler_file = f"{model_name}_scaler.joblib"
        
        if os.path.exists(os.path.join(MODEL_DIR, metrics_file)):
            import json
            with open(os.path.join(MODEL_DIR, metrics_file), 'r') as f:
                metrics = json.load(f)
            models[f"{model_name}_nn"] = {
                'type': 'neural_network',
                'file': model_file,
                'scaler_file': scaler_file if os.path.exists(os.path.join(MODEL_DIR, scaler_file)) else None,
                'metrics': metrics
            }
    
    return models

def load_model(model_name):
    """
    Carga un modelo guardado.
    
    Args:
        model_name: Nombre del modelo a cargar
        
    Returns:
        model: Modelo cargado
        scaler: Escalador asociado (si existe)
    """
    if not os.path.exists(MODEL_DIR):
        raise FileNotFoundError(f"Directorio de modelos no encontrado: {MODEL_DIR}")
    
    # Verificar si es un modelo joblib
    model_joblib_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")
    if os.path.exists(model_joblib_path):
        model = joblib.load(model_joblib_path)
        # Buscar scaler por separado
        scaler_path = os.path.join(MODEL_DIR, f"{model_name}_scaler.joblib")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            return model, scaler
        else:
            return model, None
    
    # Verificar si es un modelo de red neuronal (.keras)
    model_keras_path = os.path.join(MODEL_DIR, f"{model_name}.keras")
    if os.path.exists(model_keras_path):
        if not HAS_TENSORFLOW:
            raise ImportError("TensorFlow no está disponible para cargar modelos de redes neuronales")
        
        model = keras.models.load_model(model_keras_path)
        # Cargar scaler
        scaler_path = os.path.join(MODEL_DIR, f"{model_name.replace('_nn', '')}_scaler.joblib")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            return model, scaler
        else:
            return model, None
    
    raise FileNotFoundError(f"Modelo no encontrado: {model_name}")

def predict_fare(df, features=None, model_name=None):
    """
    Predice el costo del viaje utilizando el modelo entrenado.
    
    Args:
        df: DataFrame con los datos para la predicción
        features: Lista de características para usar (si es None, usa todas las disponibles)
        model_name: Nombre específico del modelo a usar (si es None, usa el mejor disponible)
        
    Returns:
        array: Predicciones de costo
    """
    # Si no se especifica modelo, usar el mejor disponible para predicción de tarifas
    if model_name is None:
        available_models = get_available_models()
        fare_models = [name for name in available_models.keys() if 'driver_pay' in name]
        
        if not fare_models:
            print("No hay modelos de predicción de tarifas disponibles")
            return None
            
        # Preferir Random Forest, luego LightGBM, luego Red Neuronal
        if 'driver_pay_rf' in fare_models:
            model_name = 'driver_pay_rf'
        elif 'driver_pay_lgb' in fare_models:
            model_name = 'driver_pay_lgb'
        elif 'driver_pay_nn' in fare_models:
            model_name = 'driver_pay_nn'
        else:
            model_name = fare_models[0]
    
    try:
        model, scaler = load_model(model_name)
        
        # Preparar características básicas si no se especifican
        if features is None:
            # Características básicas que esperan los modelos
            basic_features = ['trip_miles', 'trip_time', 'pickup_hour']
            features = [f for f in basic_features if f in df.columns]
        
        # Filtrar DataFrame para incluir solo las características disponibles
        available_features = [f for f in features if f in df.columns]
        
        if len(available_features) == 0:
            print(f"Ninguna característica disponible para predicción")
            return None
        
        df_filtered = df[available_features].copy()
        
        # Si es un modelo de red neuronal y hay scaler, aplicar escalado
        if model_name.endswith('_nn') and scaler is not None:
            X_processed = scaler.transform(df_filtered)
            predictions = model.predict(X_processed)
            return predictions.flatten()
        else:
            # Para modelos tradicionales
            predictions = model.predict(df_filtered)
            return predictions
    
    except Exception as e:
        print(f"Error al predecir con el modelo {model_name}: {e}")
        return None

def predict_airport(df, features=None):
    """
    Clasifica si un viaje es a/desde un aeropuerto.
    
    Args:
        df: DataFrame con los datos para la clasificación
        features: Lista de características para usar (si es None, usa todas las disponibles)
        
    Returns:
        array: Predicciones binarias (1 = aeropuerto, 0 = no aeropuerto)
        array: Probabilidades para la clase positiva
    """
    model_name = 'airport_classifier'
    
    try:
        model, _ = load_model(model_name)
        
        # Obtener las características que el modelo espera
        required_features = []
        if hasattr(model, 'feature_names_in_'):
            required_features = model.feature_names_in_.tolist()
        elif hasattr(model, 'feature_names'):
            required_features = model.feature_names
        
        # Filtrar el DataFrame para incluir solo las características requeridas
        if required_features:
            # Verificar qué características están disponibles
            available_features = [f for f in required_features if f in df.columns]
            
            if len(available_features) == 0:
                print(f"Ninguna de las características requeridas está disponible. Requeridas: {required_features}")
                # Usar las características más básicas como fallback
                if all(col in df.columns for col in ['trip_miles', 'trip_time']):
                    available_features = ['trip_miles', 'trip_time']
            
            # Usar solo las características disponibles
            df_filtered = df[available_features].copy()
        else:
            # Si no hay información de características, usar el df tal cual
            df_filtered = df.copy()
            
            # Si se especifican características explícitamente, filtrar el df
            if features is not None:
                valid_features = [f for f in features if f in df.columns]
                df_filtered = df[valid_features].copy()
        
        # Realizar predicción
        predictions = model.predict(df_filtered)
        
        # Obtener probabilidades si el modelo lo soporta
        try:
            probabilities = model.predict_proba(df_filtered)[:, 1]  # Probabilidad para la clase positiva
        except:
            probabilities = None
        
        return predictions, probabilities
    
    except Exception as e:
        print(f"Error al predecir con el modelo {model_name}: {e}")
        
        # Si falla el modelo tradicional, intentar con la red neuronal
        try:
            model_name = 'airport_nn'
            model, preprocessor = load_model(model_name)
            
            # Si se especifican características, filtrar el df
            if features is not None:
                df = df[features].copy()
            
            # Preprocesar datos y predecir
            X_processed = preprocessor.transform(df)
            
            # Obtener probabilidades y predicciones
            if model.output_shape[-1] == 1:  # Modelo binario
                probs = model.predict(X_processed).flatten()
                preds = (probs > 0.5).astype(int)
                return preds, probs
            else:  # Modelo multiclase
                probs = model.predict(X_processed)
                preds = np.argmax(probs, axis=1)
                return preds, probs[:, 1] if probs.shape[1] > 1 else probs
        
        except Exception as e2:
            print(f"Error al predecir con el modelo de red neuronal: {e2}")
            # Retornar None si ambos modelos fallan
            return None, None

def predict_trip_time(df, features=None):
    """
    Predice la duración del viaje utilizando el modelo entrenado.
    
    Args:
        df: DataFrame con los datos para la predicción
        features: Lista de características para usar (si es None, usa todas las disponibles)
        
    Returns:
        array: Predicciones de duración en segundos
    """
    model_name = 'trip_time_predictor'
    
    try:
        model, _ = load_model(model_name)
        
        # Obtener las características que el modelo espera
        required_features = []
        if hasattr(model, 'feature_names_in_'):
            required_features = model.feature_names_in_.tolist()
        elif hasattr(model, 'feature_names'):
            required_features = model.feature_names
        
        # Filtrar el DataFrame para incluir solo las características requeridas
        if required_features:
            # Verificar qué características están disponibles
            available_features = [f for f in required_features if f in df.columns]
            
            if len(available_features) == 0:
                print(f"Ninguna de las características requeridas está disponible. Requeridas: {required_features}")
                # Usar las características más básicas como fallback
                if 'trip_miles' in df.columns:
                    available_features = ['trip_miles']
            
            # Usar solo las características disponibles
            df_filtered = df[available_features].copy()
        else:
            # Si no hay información de características, usar el df tal cual
            df_filtered = df.copy()
            
            # Si se especifican características explícitamente, filtrar el df
            if features is not None:
                valid_features = [f for f in features if f in df.columns]
                df_filtered = df[valid_features].copy()
        
        # Realizar predicción
        predictions = model.predict(df_filtered)
        return predictions
    
    except Exception as e:
        print(f"Error al predecir con el modelo {model_name}: {e}")
        
        # Si falla el modelo tradicional, intentar con la red neuronal
        try:
            model_name = 'trip_time_nn'
            model, preprocessor = load_model(model_name)
            
            # Si se especifican características, filtrar el df
            if features is not None:
                df = df[features].copy()
            
            # Preprocesar datos y predecir
            X_processed = preprocessor.transform(df)
            predictions = model.predict(X_processed)
            return predictions.flatten()
        
        except Exception as e2:
            print(f"Error al predecir con el modelo de red neuronal: {e2}")
            # Retornar None si ambos modelos fallan
            return None

def get_model_info():
    """
    Obtiene información sobre los modelos disponibles para mostrar en la UI.
    
    Returns:
        dict: Información sobre los modelos disponibles
    """
    models = get_available_models()
    
    if not models:
        return {
            'status': 'No hay modelos disponibles',
            'models': {}
        }
    
    model_info = {
        'status': f'Se encontraron {len(models)} modelos',
        'models': {}
    }
    
    for name, data in models.items():
        # Extraer información de métricas relevante según el tipo de modelo
        metrics = data.get('metrics', {})
        
        if 'driver_pay' in name:
            model_type = 'Predicción de tarifa'
            if 'rmse' in metrics:
                performance = f"RMSE: {metrics['rmse']:.4f}"
            elif 'r2' in metrics:
                performance = f"R²: {metrics['r2']:.4f}"
            else:
                performance = "No hay métricas disponibles"
                
        elif 'airport' in name:
            model_type = 'Clasificación de viajes a aeropuertos'
            if 'accuracy' in metrics:
                performance = f"Precisión: {metrics['accuracy']:.4f}"
            else:
                performance = "No hay métricas disponibles"
                
        elif 'trip_time' in name:
            model_type = 'Predicción de duración'
            if 'rmse' in metrics:
                performance = f"RMSE: {metrics['rmse']:.4f}"
            elif 'r2' in metrics:
                performance = f"R²: {metrics['r2']:.4f}"
            else:
                performance = "No hay métricas disponibles"
                
        else:
            model_type = 'Otro'
            performance = "Métricas no definidas"
        
        model_info['models'][name] = {
            'type': model_type,
            'performance': performance,
            'tech': 'Red Neuronal' if 'nn' in name else ('XGBoost' if 'best_model' in metrics and metrics['best_model'] == 'XGBoost' else 'RandomForest')
        }
    
    return model_info

def get_feature_importance(model_name):
    """
    Obtiene la importancia de las características para un modelo.
    Solo funciona para modelos basados en árboles (RandomForest, XGBoost).
    
    Args:
        model_name: Nombre del modelo
        
    Returns:
        dict: Diccionario con las características y su importancia
    """
    try:
        model, preprocessor = load_model(model_name)
        
        # Verificar si es un pipeline
        if hasattr(model, 'named_steps'):
            # Obtener el modelo real (no el pipeline)
            if 'regressor' in model.named_steps:
                model_component = model.named_steps['regressor']
            elif 'classifier' in model.named_steps:
                model_component = model.named_steps['classifier']
            else:
                return None
        else:
            model_component = model
        
        # Obtener importancia de características
        if hasattr(model_component, 'feature_importances_'):
            importances = model_component.feature_importances_
            
            # Obtener nombres de características
            if preprocessor is not None and hasattr(preprocessor, 'get_feature_names_out'):
                try:
                    feature_names = preprocessor.get_feature_names_out()
                except:
                    # Para versiones antiguas de scikit-learn
                    feature_names = [f"feature_{i}" for i in range(len(importances))]
            else:
                feature_names = [f"feature_{i}" for i in range(len(importances))]
            
            # Crear y ordenar diccionario de importancias
            importance_dict = dict(zip(feature_names, importances))
            importance_dict = {k: v for k, v in sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)}
            
            return importance_dict
        
        return None
    
    except Exception as e:
        print(f"Error al obtener importancia de características: {e}")
        return None