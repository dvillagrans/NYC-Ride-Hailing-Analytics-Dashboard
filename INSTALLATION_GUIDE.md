# 🛠️ Guía de Instalación Completa

> **Guía paso a paso para configurar el NYC Ride-Hailing Analytics Dashboard**

## 📋 Tabla de Contenidos

- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación Básica](#-instalación-básica)
- [Configuración de GPU (Opcional)](#-configuración-de-gpu-opcional)
- [Configuración de Datos](#-configuración-de-datos)
- [Entrenamiento de Modelos](#-entrenamiento-de-modelos)
- [Verificación de Instalación](#-verificación-de-instalación)
- [Solución de Problemas](#-solución-de-problemas)
- [Configuración para Producción](#-configuración-para-producción)

## 💻 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 o superior
- **RAM**: 8 GB mínimo (16 GB recomendado)
- **Almacenamiento**: 5 GB de espacio libre
- **Procesador**: Intel i5 o AMD Ryzen 5 (o equivalente)

### Requisitos Recomendados
- **RAM**: 16 GB o más
- **GPU**: NVIDIA GTX 1060 o superior (para modelos ML avanzados)
- **SSD**: Para mejor rendimiento de carga de datos
- **Conexión a Internet**: Para descargar dependencias

## 🚀 Instalación Básica

### Paso 1: Verificar Python

```bash
# Verificar versión de Python
python --version
# o
python3 --version

# Debe mostrar Python 3.8 o superior
```

### Paso 2: Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/tu-usuario/nyc-ridehailing-dashboard.git
cd nyc-ridehailing-dashboard

# O descargar ZIP y extraer
# Luego navegar al directorio extraído
```

### Paso 3: Crear Entorno Virtual

#### Windows
```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verificar activación (debe mostrar (venv) al inicio)
```

#### macOS/Linux
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verificar activación (debe mostrar (venv) al inicio)
```

### Paso 4: Actualizar pip

```bash
# Actualizar pip a la última versión
python -m pip install --upgrade pip
```

### Paso 5: Instalar Dependencias

#### Instalación Estándar
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

#### Instalación Mínima (sin ML avanzado)
```bash
# Solo dependencias básicas
pip install streamlit pandas numpy plotly folium streamlit-folium pydeck pyarrow
```

#### Instalación con GPU (NVIDIA)
```bash
# Instalar TensorFlow con soporte GPU
pip install tensorflow-gpu>=2.13.0

# Verificar instalación GPU
python -c "import tensorflow as tf; print('GPU disponible:', tf.config.list_physical_devices('GPU'))"
```

## 🎮 Configuración de GPU (Opcional)

### Para NVIDIA GPUs

#### 1. Instalar CUDA Toolkit
- Descargar desde [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- Instalar versión compatible con TensorFlow (CUDA 11.8 recomendado)

#### 2. Instalar cuDNN
- Descargar desde [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)
- Extraer y copiar archivos a directorio CUDA

#### 3. Configurar Variables de Entorno

**Windows:**
```cmd
set CUDA_VISIBLE_DEVICES=0
set TF_FORCE_GPU_ALLOW_GROWTH=true
```

**Linux/macOS:**
```bash
export CUDA_VISIBLE_DEVICES=0
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

#### 4. Verificar Configuración GPU
```python
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("GPU disponible:", tf.config.list_physical_devices('GPU'))
print("CUDA build:", tf.test.is_built_with_cuda())
```

### Para Apple Silicon (M1/M2)

```bash
# Instalar TensorFlow optimizado para Apple Silicon
pip install tensorflow-macos>=2.13.0
pip install tensorflow-metal>=1.0.0
```

## 📊 Configuración de Datos

### Estructura de Datos Requerida

```
data/
├── taxi_zone_lookup.csv      # Información de zonas NYC
├── taxi_zone_centroids.csv   # Coordenadas de centroides
data_sampled/
├── 2024-01_reduced.parquet   # Datos mensuales procesados
├── 2024-02_reduced.parquet
└── ...
```

### Obtener Datos de Muestra

#### Opción 1: Datos Incluidos
Los datos de muestra ya están incluidos en el repositorio.

#### Opción 2: Generar Nuevos Datos
```bash
# Descargar datos originales (requiere ~10GB)
python scripts/download_data.py

# Procesar y crear muestras
python generate_reduced_parquets.py
```

#### Opción 3: Usar Datos Personalizados
1. Colocar archivos `.parquet` en `data_sampled/`
2. Seguir formato: `YYYY-MM_reduced.parquet`
3. Asegurar columnas requeridas:
   - `pickup_datetime`
   - `hvfhs_license_num`
   - `PULocationID`
   - `DOLocationID`
   - `driver_pay`
   - `tips`

## 🤖 Entrenamiento de Modelos

### Modelos Básicos (CPU)
```bash
# Entrenar modelos con scikit-learn
python train_models_no_tf.py

# Tiempo estimado: 5-15 minutos
```

### Modelos Avanzados (GPU)
```bash
# Entrenar con TensorFlow y GPU
python train_models.py

# Tiempo estimado: 2-10 minutos con GPU
```

### Modelos de Demostración
```bash
# Crear modelos rápidos para testing
python create_demo_models.py

# Tiempo estimado: 1-3 minutos
```

### Verificar Modelos Entrenados
```bash
# Listar modelos disponibles
ls models/

# Debe mostrar:
# - driver_pay_predictor.joblib
# - airport_classifier.joblib
# - trip_time_predictor.joblib
# - *_metrics.joblib (métricas de cada modelo)
```

## ✅ Verificación de Instalación

### Test Básico
```bash
# Ejecutar dashboard
streamlit run app.py

# Debe abrir navegador en http://localhost:8501
```

### Test de Funcionalidades
```python
# Crear archivo test_installation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import model_utils

print("✅ Streamlit:", st.__version__)
print("✅ Pandas:", pd.__version__)
print("✅ Plotly:", px.__version__)

# Test modelos ML
try:
    models = model_utils.get_available_models()
    print(f"✅ Modelos ML: {len(models)} disponibles")
except:
    print("⚠️ Modelos ML: No disponibles (entrenar primero)")

print("🎉 Instalación completada exitosamente!")
```

```bash
# Ejecutar test
python test_installation.py
```

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Verificar entorno virtual activado
which python  # Linux/macOS
where python  # Windows

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "CUDA out of memory"
```python
# Reducir batch size en entrenamiento
# Editar train_models.py:
# batch_size = 32  # Reducir de 128 a 32
```

### Error: "Streamlit command not found"
```bash
# Verificar instalación
pip show streamlit

# Reinstalar si es necesario
pip install streamlit --upgrade
```

### Error: "Permission denied" (Linux/macOS)
```bash
# Dar permisos de ejecución
chmod +x scripts/*.py

# O ejecutar con python explícitamente
python scripts/train_models.py
```

### Error: "Port already in use"
```bash
# Usar puerto diferente
streamlit run app.py --server.port 8502

# O matar proceso existente
# Windows: taskkill /f /im streamlit.exe
# Linux/macOS: pkill -f streamlit
```

### Problemas de Memoria
```bash
# Reducir tamaño de datos
# Editar app.py para usar menos archivos:
# data_files = data_files[:2]  # Solo 2 meses

# O aumentar memoria virtual (swap)
```

## 🌐 Configuración para Producción

### Usando Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Construir imagen
docker build -t nyc-dashboard .

# Ejecutar contenedor
docker run -p 8501:8501 nyc-dashboard
```

### Usando Streamlit Cloud

1. Subir código a GitHub
2. Conectar repositorio en [Streamlit Cloud](https://streamlit.io/cloud)
3. Configurar variables de entorno si es necesario
4. Deploy automático

### Configuración de Servidor

```bash
# Instalar en servidor Linux
sudo apt update
sudo apt install python3-pip python3-venv

# Clonar y configurar
git clone [repo-url]
cd nyc-ridehailing-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ejecutar como servicio
nohup streamlit run app.py --server.port 8501 &
```

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. **Revisa los logs**: Streamlit muestra errores detallados en terminal
2. **Verifica versiones**: Asegúrate de usar versiones compatibles
3. **Consulta documentación**: Links en README principal
4. **Reporta issues**: Crea un issue en GitHub con:
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir

---

<div align="center">
  <strong>🚀 ¡Listo para analizar datos de transporte urbano! 🚀</strong>
</div>