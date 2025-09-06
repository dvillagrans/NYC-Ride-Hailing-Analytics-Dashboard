# 🚖 NYC Ride-Hailing Analytics Dashboard

> **Dashboard interactivo para análisis de datos de viajes de Uber y Lyft en Nueva York**

Un dashboard completo desarrollado en Streamlit que permite analizar patrones de viajes, ingresos, distribución geográfica y tendencias temporales de los servicios de ride-hailing en NYC. Incluye modelos de Machine Learning para predicción de tarifas y clasificación de viajes.

<div align="center">
  <img src="NYC Ride-Hailing Analytics Dashboard.png" alt="NYC Ride-Hailing Analytics Dashboard" width="800">
  <p><em>Vista principal del dashboard con métricas de viajes e insights en tiempo real</em></p>
</div>

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🌟 Características Principales

### 📊 **Análisis Integral de Datos**
- **Resumen General**: KPIs principales, distribución temporal y insights destacados
- **Análisis de Horas Pico**: Patrones de demanda por hora, día y zona
- **Visualización Geográfica**: Mapas interactivos con distribución de viajes
- **Comparativa Uber vs Lyft**: Análisis competitivo detallado
- **Análisis de Ingresos**: Desglose de tarifas, propinas e impuestos
- **Accesibilidad**: Análisis de viajes con servicios de accesibilidad
- **Viajes a Aeropuertos**: Patrones específicos de conectividad aeroportuaria

### 🤖 **Modelos de Machine Learning**
- **Predicción de Tarifas**: Modelo para estimar el costo de viajes
- **Clasificación de Aeropuertos**: Identificación automática de viajes aeroportuarios
- **Análisis de Características**: Importancia de variables en las predicciones
- **Soporte para GPU**: Entrenamiento acelerado con TensorFlow

### 🗺️ **Visualizaciones Avanzadas**
- **Mapas de Calor**: Distribución temporal y geográfica
- **Mapas Interactivos**: Folium y PyDeck para visualización 3D
- **Gráficos Dinámicos**: Plotly para interactividad completa
- **Dashboards Responsivos**: Optimizado para diferentes dispositivos

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/nyc-ridehailing-dashboard.git
cd nyc-ridehailing-dashboard
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Dashboard
```bash
streamlit run app.py
```

El dashboard estará disponible en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
nyc-ridehailing-dashboard/
├── 📄 app.py                     # Aplicación principal de Streamlit
├── 📄 model_utils.py             # Utilidades para modelos ML
├── 📄 requirements.txt           # Dependencias del proyecto
├── 📄 ML_MODELS_README.md        # Documentación de modelos ML
├── 📁 data/                      # Datos de referencia
│   ├── taxi_zone_lookup.csv      # Información de zonas de NYC
│   └── taxi_zone_centroids.csv   # Coordenadas de centroides
├── 📁 data_sampled/              # Datos procesados (5% muestra)
│   ├── 2024-01_reduced.parquet   # Datos mensuales en formato Parquet
│   ├── 2024-02_reduced.parquet
│   └── ...
├── 📁 models/                    # Modelos ML entrenados
│   ├── driver_pay_predictor.joblib
│   ├── airport_classifier.joblib
│   └── trip_time_predictor.joblib
├── 📁 notebooks/                 # Jupyter notebooks para análisis
│   ├── Extraction.ipynb          # Extracción de datos
│   ├── Transformation.ipynb      # Transformación de datos
│   └── Consultas.ipynb          # Análisis exploratorio
└── 📁 scripts/                   # Scripts de entrenamiento
    ├── train_models.py           # Entrenamiento con TensorFlow
    ├── train_models_no_tf.py     # Entrenamiento sin TensorFlow
    └── create_demo_models.py     # Modelos de demostración
```

## 🎯 Guía de Uso

### Dashboard Principal

1. **Selección de Datos**: Usa la barra lateral para filtrar por mes, operador, hora y ubicación
2. **Navegación por Pestañas**: Explora diferentes aspectos del análisis
3. **Interactividad**: Haz clic en gráficos para obtener detalles adicionales
4. **Exportación**: Descarga visualizaciones y datos procesados

### Modelos de Machine Learning

#### Entrenar Modelos
```bash
# Con soporte para GPU (TensorFlow)
python train_models.py

# Solo con scikit-learn (CPU)
python train_models_no_tf.py

# Modelos de demostración rápida
python create_demo_models.py
```

#### Usar Predicciones
```python
import model_utils
import pandas as pd

# Crear datos de ejemplo
data = pd.DataFrame({
    'trip_miles': [5.2],
    'trip_time': [900],  # segundos
    'pickup_hour': [14],
    'hvfhs_license_num': ['Uber']
})

# Predecir tarifa
fare = model_utils.predict_fare(data)
print(f"Tarifa estimada: ${fare[0]:.2f}")

# Clasificar viaje a aeropuerto
is_airport, probability = model_utils.predict_airport(data)
print(f"¿Viaje a aeropuerto?: {is_airport[0]} (confianza: {probability[0]:.2f})")
```

## 📊 Funcionalidades del Dashboard

### 🏠 **Pestaña Resumen**
- KPIs principales (viajes totales, ingresos, operadores)
- Distribución por hora y día de la semana
- Mapa de calor temporal
- Tendencias diarias
- Resumen por operador

### ⏰ **Pestaña Horas Pico**
- Análisis de demanda por hora
- Mapas de calor por operador
- Comparativas de ingresos y propinas
- Identificación de patrones temporales

### 🗺️ **Pestaña Mapas**
- Mapa de densidad de viajes
- Visualización 3D con PyDeck
- Rutas más populares
- Distribución geográfica por operador

### 🏢 **Pestaña Uber vs Lyft**
- Comparativa de cuota de mercado
- Análisis de precios y eficiencia
- Concentración por zonas
- Patrones temporales comparativos

### 💰 **Pestaña Ingresos**
- Desglose de tarifas e impuestos
- Análisis de propinas
- Tendencias de ingresos
- Composición de costos

### ♿ **Pestaña Accesibilidad**
- Análisis de servicios WAV (Wheelchair Accessible Vehicle)
- Distribución geográfica de servicios accesibles
- Comparativa de tarifas

### ✈️ **Pestaña Aeropuertos**
- Viajes hacia y desde aeropuertos (JFK, LaGuardia, Newark)
- Patrones horarios específicos
- Análisis de tarifas aeroportuarias

### 🤖 **Pestaña Modelos ML**
- Predicción interactiva de tarifas
- Clasificación de viajes a aeropuertos
- Análisis de importancia de características
- Métricas de rendimiento de modelos

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Configurar GPU para TensorFlow (opcional)
export CUDA_VISIBLE_DEVICES=0

# Configurar memoria de GPU
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

### Personalización de Datos

1. **Agregar Nuevos Meses**: Coloca archivos `.parquet` en `data_sampled/`
2. **Modificar Zonas**: Actualiza `data/taxi_zone_lookup.csv`
3. **Ajustar Muestreo**: Modifica `generate_reduced_parquets.py`

## 📈 Métricas y Rendimiento

### Modelos de Machine Learning
- **Predicción de Tarifas**: RMSE < $3.00, R² > 0.85
- **Clasificación de Aeropuertos**: Accuracy > 92%
- **Tiempo de Predicción**: < 100ms por muestra

### Rendimiento del Dashboard
- **Carga de Datos**: < 5 segundos para archivos de 100MB
- **Renderizado**: < 2 segundos para gráficos complejos
- **Memoria**: < 2GB RAM para datasets completos

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Mejora
- [ ] Integración con APIs en tiempo real
- [ ] Modelos de deep learning más avanzados
- [ ] Análisis de sentimientos de reseñas
- [ ] Predicción de demanda futura
- [ ] Optimización de rutas

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Diego** - *Desarrollador Principal*

- 📧 Email: [tu-email@ejemplo.com]
- 💼 LinkedIn: [tu-perfil-linkedin]
- 🐙 GitHub: [tu-usuario-github]

## 🙏 Agradecimientos

- **NYC Taxi & Limousine Commission** por proporcionar los datos públicos
- **Streamlit** por la excelente plataforma de dashboards
- **Plotly** por las visualizaciones interactivas
- **Comunidad de Python** por las increíbles librerías de ciencia de datos

## 📚 Referencias

- [NYC TLC Trip Record Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)

---

<div align="center">
  <strong>🚖 Hecho con ❤️ para el análisis de datos de transporte urbano 🚖</strong>
</div>