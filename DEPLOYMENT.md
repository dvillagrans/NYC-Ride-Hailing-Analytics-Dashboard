# 🚀 Deployment Guide - NYC Ride-Hailing Analytics Dashboard

## 📋 Pre-deployment Checklist

✅ **Archivos de configuración creados:**
- `.streamlit/config.toml` - Configuración de tema y servidor
- `packages.txt` - Dependencias del sistema
- `requirements.txt` - Dependencias de Python

✅ **Datos de muestra preparados:**
- `data/2024-02_reduced.parquet` - Dataset principal (100k registros)
- `data/taxi_zone_lookup.csv` - Información de zonas
- `data/taxi_zone_centroids.csv` - Coordenadas de zonas

✅ **Aplicación probada localmente:**
- Streamlit funciona correctamente
- Datos se cargan sin errores
- Visualizaciones se renderizan

## 🌐 Deployment en Streamlit Community Cloud

### Paso 1: Preparar el repositorio
1. Asegúrate de que todos los archivos estén en el repositorio de GitHub
2. Los archivos de datos deben estar incluidos (no están en .gitignore)
3. Verifica que `requirements.txt` esté actualizado

### Paso 2: Conectar con Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona el repositorio: `NYC-Ride-Hailing-Analytics-Dashboard`
4. Especifica el archivo principal: `app.py`
5. Rama: `main` (o la rama principal)

### Paso 3: Configuración avanzada (opcional)
- **Python version**: 3.9+
- **Secrets**: No requeridos para este proyecto
- **Environment variables**: No requeridos

### Paso 4: Deploy
1. Haz clic en "Deploy!"
2. Espera a que se complete la instalación de dependencias
3. La aplicación estará disponible en una URL como: `https://your-app-name.streamlit.app`

## 🔧 Solución de problemas comunes

### Error de memoria
Si la aplicación falla por memoria:
- Reduce el tamaño del dataset en `data/2024-02_reduced.parquet`
- Ejecuta `extract_data.py` con un porcentaje menor (ej: 3%)

### Dependencias faltantes
Si faltan paquetes del sistema:
- Verifica `packages.txt`
- Añade dependencias adicionales si es necesario

### Errores de datos
Si hay problemas con los datos:
- Verifica que los archivos CSV tengan las columnas correctas
- Ejecuta `extract_data.py` nuevamente para regenerar datos

## 📊 Características del deployment

- **Dataset**: 100,000 registros de viajes de febrero 2024
- **Tamaño**: ~5MB de datos
- **Rendimiento**: Optimizado para Streamlit Cloud
- **Funcionalidades**: Todas las características originales habilitadas

## 🎯 URLs importantes

- **Aplicación local**: http://localhost:8501
- **Repositorio**: [Tu repositorio de GitHub]
- **Streamlit Cloud**: [URL después del deployment]

## 📝 Notas adicionales

- Los datos son una muestra representativa del dataset completo
- La aplicación mantiene todas las funcionalidades originales
- El rendimiento está optimizado para deployment en la nube
- Se incluyen archivos de configuración para mejor experiencia de usuario