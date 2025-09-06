# 🤝 Guía de Contribución

> **Cómo contribuir al NYC Ride-Hailing Analytics Dashboard**

¡Gracias por tu interés en contribuir a este proyecto! Esta guía te ayudará a entender cómo puedes participar y mejorar el dashboard.

## 📋 Tabla de Contenidos

- [Código de Conducta](#-código-de-conducta)
- [Cómo Contribuir](#-cómo-contribuir)
- [Configuración del Entorno](#-configuración-del-entorno)
- [Estándares de Código](#-estándares-de-código)
- [Proceso de Pull Request](#-proceso-de-pull-request)
- [Reportar Issues](#-reportar-issues)
- [Áreas de Mejora](#-áreas-de-mejora)
- [Reconocimientos](#-reconocimientos)

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de la participación en nuestro proyecto una experiencia libre de acoso para todos, independientemente de:

- Edad, tamaño corporal, discapacidad visible o invisible
- Etnia, características sexuales, identidad y expresión de género
- Nivel de experiencia, educación, estatus socioeconómico
- Nacionalidad, apariencia personal, raza, religión
- Identidad y orientación sexual

### Comportamiento Esperado

- ✅ Usar lenguaje acogedor e inclusivo
- ✅ Respetar diferentes puntos de vista y experiencias
- ✅ Aceptar críticas constructivas con gracia
- ✅ Enfocarse en lo que es mejor para la comunidad
- ✅ Mostrar empatía hacia otros miembros

### Comportamiento Inaceptable

- ❌ Uso de lenguaje o imágenes sexualizadas
- ❌ Trolling, comentarios insultantes o ataques personales
- ❌ Acoso público o privado
- ❌ Publicar información privada sin permiso
- ❌ Cualquier conducta inapropiada en un entorno profesional

## 🚀 Cómo Contribuir

### Tipos de Contribuciones

#### 🐛 **Reportar Bugs**
- Usa el template de issue para bugs
- Incluye pasos para reproducir
- Proporciona información del sistema
- Adjunta screenshots si es relevante

#### 💡 **Sugerir Mejoras**
- Usa el template de feature request
- Explica el problema que resuelve
- Describe la solución propuesta
- Considera alternativas

#### 📝 **Mejorar Documentación**
- Corregir errores tipográficos
- Clarificar instrucciones confusas
- Agregar ejemplos
- Traducir a otros idiomas

#### 🔧 **Contribuir Código**
- Implementar nuevas funcionalidades
- Optimizar rendimiento
- Refactorizar código existente
- Agregar tests

#### 📊 **Agregar Datos**
- Nuevos datasets
- Datos de validación
- Casos de prueba
- Benchmarks

## 🛠️ Configuración del Entorno

### Configuración para Desarrollo

#### 1. Fork y Clone
```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/nyc-ridehailing-dashboard.git
cd nyc-ridehailing-dashboard

# Agregar upstream remote
git remote add upstream https://github.com/USUARIO-ORIGINAL/nyc-ridehailing-dashboard.git
```

#### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

#### 3. Instalar Pre-commit Hooks
```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
pre-commit install

# Ejecutar en todos los archivos (opcional)
pre-commit run --all-files
```

#### 4. Configurar Variables de Entorno
```bash
# Crear archivo .env
cp .env.example .env

# Editar variables según tu configuración
# STREAMLIT_SERVER_PORT=8501
# CUDA_VISIBLE_DEVICES=0
# TF_FORCE_GPU_ALLOW_GROWTH=true
```

### Estructura de Desarrollo

```
nyc-ridehailing-dashboard/
├── 📁 .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── PULL_REQUEST_TEMPLATE.md
├── 📁 docs/
│   ├── api/
│   ├── tutorials/
│   └── examples/
├── 📁 tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── 📁 scripts/
│   ├── setup/
│   ├── data_processing/
│   └── deployment/
├── 📄 .pre-commit-config.yaml
├── 📄 requirements-dev.txt
├── 📄 pytest.ini
└── 📄 .env.example
```

## 📏 Estándares de Código

### Estilo de Código Python

#### Formateo
```bash
# Usar Black para formateo automático
black .

# Configuración en pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
```

#### Linting
```bash
# Usar flake8 para linting
flake8 .

# Configuración en .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = venv/, .git/, __pycache__/
```

#### Imports
```python
# Orden de imports (isort)
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third party
import pandas as pd
import numpy as np
import streamlit as st

# 3. Local imports
from model_utils import load_model
from utils.data_processing import preprocess_data
```

### Convenciones de Naming

#### Variables y Funciones
```python
# Snake case para variables y funciones
user_data = load_user_data()
total_trips = calculate_total_trips(df)

def process_trip_data(raw_data):
    """Procesa datos de viajes."""
    pass
```

#### Clases
```python
# Pascal case para clases
class TripDataProcessor:
    """Procesador de datos de viajes."""
    
    def __init__(self, config):
        self.config = config
```

#### Constantes
```python
# Upper case para constantes
MAX_TRIP_DISTANCE = 100
DEFAULT_TIMEOUT = 30
AIRPORT_ZONES = [1, 132, 138]
```

### Documentación de Código

#### Docstrings
```python
def predict_fare(trip_data, model_name="default"):
    """
    Predice la tarifa de un viaje usando ML.
    
    Args:
        trip_data (pd.DataFrame): Datos del viaje con columnas requeridas.
        model_name (str, optional): Nombre del modelo a usar. Default "default".
    
    Returns:
        np.ndarray: Array con predicciones de tarifa.
    
    Raises:
        ValueError: Si faltan columnas requeridas.
        ModelNotFoundError: Si el modelo no existe.
    
    Example:
        >>> data = pd.DataFrame({'trip_miles': [5.0], 'trip_time': [900]})
        >>> predictions = predict_fare(data)
        >>> print(f"Tarifa estimada: ${predictions[0]:.2f}")
    """
    pass
```

#### Comentarios
```python
# Comentarios para lógica compleja
def complex_calculation(data):
    # Aplicar transformación logarítmica para normalizar distribución
    log_data = np.log1p(data)
    
    # Calcular percentiles para detección de outliers
    q25, q75 = np.percentile(log_data, [25, 75])
    iqr = q75 - q25
    
    # Filtrar outliers usando regla IQR
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    
    return log_data[(log_data >= lower_bound) & (log_data <= upper_bound)]
```

### Testing

#### Estructura de Tests
```python
# tests/test_model_utils.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from model_utils import predict_fare, load_model

class TestPredictFare:
    """Tests para función predict_fare."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.sample_data = pd.DataFrame({
            'trip_miles': [5.0, 10.0],
            'trip_time': [900, 1800],
            'pickup_hour': [14, 18]
        })
    
    def test_predict_fare_success(self):
        """Test predicción exitosa."""
        with patch('model_utils.load_model') as mock_load:
            mock_model = MagicMock()
            mock_model.predict.return_value = [25.50, 45.75]
            mock_load.return_value = (mock_model, None)
            
            result = predict_fare(self.sample_data)
            
            assert len(result) == 2
            assert result[0] == 25.50
            assert result[1] == 45.75
    
    def test_predict_fare_missing_columns(self):
        """Test con columnas faltantes."""
        incomplete_data = pd.DataFrame({'trip_miles': [5.0]})
        
        with pytest.raises(ValueError, match="Missing required columns"):
            predict_fare(incomplete_data)
    
    @pytest.mark.parametrize("trip_miles,expected_range", [
        (1.0, (5, 15)),
        (10.0, (25, 50)),
        (20.0, (50, 100))
    ])
    def test_fare_ranges(self, trip_miles, expected_range):
        """Test rangos esperados de tarifas."""
        data = pd.DataFrame({
            'trip_miles': [trip_miles],
            'trip_time': [trip_miles * 120],  # Aproximación
            'pickup_hour': [14]
        })
        
        result = predict_fare(data)
        assert expected_range[0] <= result[0] <= expected_range[1]
```

#### Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Tests específicos
pytest tests/test_model_utils.py::TestPredictFare::test_predict_fare_success

# Con verbose output
pytest -v
```

## 🔄 Proceso de Pull Request

### Antes de Crear PR

#### 1. Sincronizar con Upstream
```bash
# Actualizar main local
git checkout main
git fetch upstream
git merge upstream/main

# Push a tu fork
git push origin main
```

#### 2. Crear Branch de Feature
```bash
# Crear branch descriptivo
git checkout -b feature/add-real-time-data
# o
git checkout -b fix/memory-leak-in-data-loading
# o
git checkout -b docs/improve-installation-guide
```

#### 3. Desarrollar y Commitear
```bash
# Commits atómicos con mensajes descriptivos
git add .
git commit -m "feat: add real-time data integration

- Implement WebSocket connection to TLC API
- Add real-time data processing pipeline
- Update dashboard to show live updates
- Add configuration for refresh intervals

Closes #123"
```

### Convenciones de Commit

#### Formato
```
type(scope): description

[optional body]

[optional footer]
```

#### Tipos
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo, sin cambios de lógica
- `refactor`: Refactoring sin cambios funcionales
- `test`: Agregar o modificar tests
- `chore`: Mantenimiento, dependencias

#### Ejemplos
```bash
# Feature nueva
git commit -m "feat(ml): add XGBoost model for fare prediction"

# Bug fix
git commit -m "fix(dashboard): resolve memory leak in data caching"

# Documentación
git commit -m "docs(readme): add installation instructions for Windows"

# Refactoring
git commit -m "refactor(utils): extract data validation to separate module"
```

### Template de Pull Request

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## ¿Cómo se ha probado?
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Pruebas manuales
- [ ] Tests en diferentes navegadores

## Checklist
- [ ] Mi código sigue las convenciones del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban mi fix/feature
- [ ] Tests nuevos y existentes pasan localmente

## Screenshots (si aplica)
[Agregar screenshots de cambios UI]

## Issues Relacionados
Closes #123
Related to #456
```

### Proceso de Review

#### Para Reviewers
1. **Funcionalidad**: ¿El código hace lo que dice?
2. **Calidad**: ¿Sigue las convenciones?
3. **Tests**: ¿Está adecuadamente probado?
4. **Documentación**: ¿Está documentado?
5. **Rendimiento**: ¿Impacta negativamente?

#### Para Contributors
1. **Responder Feedback**: Abordar todos los comentarios
2. **Hacer Cambios**: Implementar sugerencias
3. **Re-request Review**: Cuando esté listo
4. **Ser Paciente**: El proceso puede tomar tiempo

## 🐛 Reportar Issues

### Template de Bug Report

```markdown
**Describe el bug**
Descripción clara y concisa del problema.

**Para Reproducir**
Pasos para reproducir el comportamiento:
1. Ve a '...'
2. Haz clic en '....'
3. Scroll down to '....'
4. Ve el error

**Comportamiento Esperado**
Descripción clara de lo que esperabas que pasara.

**Screenshots**
Si aplica, agrega screenshots para explicar el problema.

**Información del Sistema:**
 - OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
 - Navegador: [e.g. Chrome 95, Firefox 94, Safari 15]
 - Versión Python: [e.g. 3.9.7]
 - Versión Streamlit: [e.g. 1.28.0]

**Contexto Adicional**
Cualquier otra información relevante sobre el problema.

**Logs de Error**
```
[Pegar logs aquí]
```
```

### Template de Feature Request

```markdown
**¿Tu feature request está relacionado con un problema?**
Descripción clara del problema. Ej: "Estoy frustrado cuando..."

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que pase.

**Describe alternativas consideradas**
Descripción de soluciones alternativas que consideraste.

**Contexto Adicional**
Cualquier otra información o screenshots sobre el feature request.

**Impacto Esperado**
- [ ] Mejora la experiencia de usuario
- [ ] Aumenta el rendimiento
- [ ] Agrega nueva funcionalidad analítica
- [ ] Mejora la accesibilidad
- [ ] Otro: ___________

**Prioridad Sugerida**
- [ ] Crítica
- [ ] Alta
- [ ] Media
- [ ] Baja
```

## 🎯 Áreas de Mejora

### 🚀 **Funcionalidades Prioritarias**

#### 1. **Integración de Datos en Tiempo Real**
- **Descripción**: Conectar con APIs de TLC para datos live
- **Complejidad**: Alta
- **Skills**: Python, APIs, WebSockets
- **Impacto**: Alto

#### 2. **Modelos ML Avanzados**
- **Descripción**: Implementar deep learning y ensemble methods
- **Complejidad**: Alta
- **Skills**: TensorFlow, PyTorch, MLOps
- **Impacto**: Alto

#### 3. **Dashboard Móvil**
- **Descripción**: Optimizar para dispositivos móviles
- **Complejidad**: Media
- **Skills**: CSS, Responsive Design
- **Impacto**: Medio

#### 4. **Análisis de Sentimientos**
- **Descripción**: Analizar reviews y feedback de usuarios
- **Complejidad**: Media
- **Skills**: NLP, APIs de redes sociales
- **Impacto**: Medio

### 🔧 **Mejoras Técnicas**

#### 1. **Optimización de Rendimiento**
- Caching más inteligente
- Lazy loading de datos
- Optimización de queries
- Paralelización de procesamiento

#### 2. **Testing y CI/CD**
- Aumentar cobertura de tests
- Tests de integración
- Automated deployment
- Performance benchmarks

#### 3. **Documentación**
- API documentation
- Video tutorials
- Jupyter notebook examples
- Traducción a otros idiomas

#### 4. **Accesibilidad**
- WCAG compliance
- Screen reader support
- Keyboard navigation
- High contrast themes

### 📊 **Nuevos Análisis**

#### 1. **Análisis Predictivo**
- Predicción de demanda
- Optimización de rutas
- Forecasting de ingresos
- Detección de anomalías

#### 2. **Análisis Geoespacial Avanzado**
- Clustering de zonas
- Análisis de flujos
- Optimización de ubicación
- Análisis de accesibilidad

#### 3. **Análisis de Sostenibilidad**
- Huella de carbono
- Eficiencia energética
- Comparación con transporte público
- Impacto ambiental

### 🎨 **Mejoras de UX/UI**

#### 1. **Personalización**
- Dashboards personalizables
- Temas customizables
- Filtros guardados
- Alertas personalizadas

#### 2. **Interactividad**
- Drill-down capabilities
- Cross-filtering
- Brushing and linking
- Real-time updates

#### 3. **Exportación Avanzada**
- Reportes automatizados
- Scheduled exports
- API endpoints
- Integration con BI tools

## 🏆 Reconocimientos

### Hall of Fame

#### 🥇 **Top Contributors**
- **Diego** - Creador y mantenedor principal
- *[Tu nombre aquí]* - Próximo gran contributor

#### 🎖️ **Categorías de Reconocimiento**

**🐛 Bug Hunters**
- Contribuidores que encuentran y reportan bugs críticos

**💡 Feature Innovators**
- Contribuidores que proponen e implementan nuevas funcionalidades

**📚 Documentation Masters**
- Contribuidores que mejoran significativamente la documentación

**🧪 Testing Champions**
- Contribuidores que mejoran la cobertura y calidad de tests

**🎨 UX/UI Designers**
- Contribuidores que mejoran la experiencia de usuario

**🚀 Performance Optimizers**
- Contribuidores que mejoran el rendimiento del sistema

### Cómo Obtener Reconocimiento

1. **Contribuciones Consistentes**: PRs regulares y de calidad
2. **Ayuda a la Comunidad**: Responder issues y ayudar a otros
3. **Innovación**: Proponer e implementar ideas creativas
4. **Calidad**: Mantener altos estándares en código y documentación
5. **Colaboración**: Trabajar bien con otros contributors

### Beneficios del Reconocimiento

- **Badge en GitHub**: Reconocimiento visible en tu perfil
- **Mención en README**: Tu nombre en la lista de contributors
- **Acceso Prioritario**: Early access a nuevas features
- **Networking**: Conexiones con otros developers
- **Portfolio**: Proyecto destacado para tu carrera

## 📞 Contacto y Soporte

### Canales de Comunicación

#### 🐙 **GitHub**
- **Issues**: Para bugs y feature requests
- **Discussions**: Para preguntas generales
- **Pull Requests**: Para contribuciones de código

#### 📧 **Email**
- **Mantenedor**: [diego@ejemplo.com]
- **Asunto**: `[NYC Dashboard] Tu consulta aquí`

#### 💬 **Chat**
- **Discord**: [Enlace al servidor] (próximamente)
- **Slack**: [Enlace al workspace] (próximamente)

### Tiempo de Respuesta Esperado

- **Issues Críticos**: 24-48 horas
- **Pull Requests**: 3-7 días
- **Feature Requests**: 1-2 semanas
- **Preguntas Generales**: 1-3 días

### Escalación

Si no recibes respuesta en el tiempo esperado:

1. **Ping en el Issue/PR**: Menciona @mantenedor
2. **Email Directo**: Para asuntos urgentes
3. **Community Help**: Otros contributors pueden ayudar

---

<div align="center">
  <strong>🤝 ¡Juntos construimos mejor software! 🤝</strong>
  
  <br><br>
  
  <em>"El código es poesía, y cada contribución es un verso que mejora la historia."</em>
</div>

---

## 📄 Licencia de Contribución

Al contribuir a este proyecto, aceptas que:

1. **Tus contribuciones** serán licenciadas bajo la misma licencia del proyecto (MIT)
2. **Tienes los derechos** para hacer la contribución
3. **Entiendes** que tus contribuciones son públicas
4. **Aceptas** el Código de Conducta del proyecto

**¡Gracias por hacer este proyecto mejor para todos!** 🎉