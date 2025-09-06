# 📖 Guía de Usuario

> **Manual completo para utilizar el NYC Ride-Hailing Analytics Dashboard**

## 📋 Tabla de Contenidos

- [Introducción](#-introducción)
- [Navegación General](#-navegación-general)
- [Pestaña Resumen](#-pestaña-resumen)
- [Pestaña Horas Pico](#-pestaña-horas-pico)
- [Pestaña Mapas](#-pestaña-mapas)
- [Pestaña Uber vs Lyft](#-pestaña-uber-vs-lyft)
- [Pestaña Ingresos](#-pestaña-ingresos)
- [Pestaña Accesibilidad](#-pestaña-accesibilidad)
- [Pestaña Aeropuertos](#-pestaña-aeropuertos)
- [Pestaña Modelos ML](#-pestaña-modelos-ml)
- [Filtros y Personalización](#-filtros-y-personalización)
- [Exportación de Datos](#-exportación-de-datos)
- [Consejos y Trucos](#-consejos-y-trucos)

## 🎯 Introducción

El **NYC Ride-Hailing Analytics Dashboard** es una herramienta interactiva que te permite analizar datos de viajes de Uber y Lyft en Nueva York. Con este dashboard puedes:

- 📊 **Analizar tendencias** de viajes por hora, día y ubicación
- 💰 **Examinar patrones de ingresos** y propinas
- 🗺️ **Visualizar distribución geográfica** de viajes
- 🤖 **Hacer predicciones** usando modelos de machine learning
- 📈 **Comparar operadores** (Uber vs Lyft)
- ✈️ **Estudiar conectividad aeroportuaria**

### Datos Utilizados

- **Fuente**: NYC Taxi & Limousine Commission (TLC)
- **Período**: 2024 (datos mensuales)
- **Muestra**: 5% de todos los viajes por operador
- **Actualización**: Los datos se procesan mensualmente

## 🧭 Navegación General

### Interfaz Principal

```
┌─────────────────────────────────────────────────────────────┐
│  🚖 NYC Dashboard                                          │
├─────────────────┬───────────────────────────────────────────┤
│                 │  📊 Resumen │ 🕐 Horas Pico │ 🗺️ Mapas    │
│   🔍 Filtros    │  💼 Uber vs Lyft │ 💰 Ingresos │ ♿ Acceso  │
│                 │  ✈️ Aeropuertos │ 🤖 Modelos ML           │
│   📅 Mes        ├───────────────────────────────────────────┤
│   🏢 Operadores │                                           │
│   🕐 Horas      │         Contenido Principal               │
│   📍 Distritos  │                                           │
│   ✈️ Aeropuertos│                                           │
└─────────────────┴───────────────────────────────────────────┘
```

### Elementos de la Interfaz

1. **Barra Superior**: Título y navegación principal
2. **Sidebar Izquierdo**: Filtros y controles
3. **Área Principal**: Contenido de la pestaña seleccionada
4. **Pestañas**: Diferentes vistas de análisis

## 📊 Pestaña Resumen

### Propósito
Ofrece una vista general de los datos con KPIs principales y tendencias básicas.

### Secciones Principales

#### 1. **KPIs Principales**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 🧾 Viajes   │ 📅 Días     │ 🏢 Operadores│ 💲 Ingresos │
│   125,432   │     31      │      4      │  $2.1M     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Cómo interpretar:**
- **Viajes**: Total de viajes en el período filtrado
- **Días únicos**: Número de días con datos
- **Operadores**: Cantidad de empresas activas
- **Ingresos Totales**: Suma de `driver_pay` (pago al conductor)

#### 2. **Insights Principales**
- **Promedio diario**: Viajes por día
- **Distancia promedio**: En millas
- **Duración promedio**: En minutos
- **Información de propinas**: Porcentaje del total

#### 3. **Distribución Temporal**

**Gráfico por Horas:**
- Muestra patrones de demanda durante el día
- Colores diferentes para cada operador
- Identifica horas pico y valle

**Gráfico por Días:**
- Compara demanda entre días de la semana
- Útil para identificar patrones laborales vs. fin de semana

#### 4. **Mapa de Calor Temporal**
- **Eje X**: Días de la semana
- **Eje Y**: Horas del día (0-23)
- **Color**: Intensidad de viajes
- **Uso**: Identificar patrones de demanda específicos

#### 5. **Tendencia Temporal**
- Solo aparece si hay datos de múltiples días
- Muestra evolución diaria del número de viajes
- Líneas separadas por operador

#### 6. **Resumen por Operador**
Tabla con métricas detalladas:
- Número de viajes
- Ingresos totales
- Propinas totales y promedio
- Porcentaje de propina
- Distancia y duración promedio (si disponible)

#### 7. **Distribución Geográfica**
- Gráfico circular por distrito (borough)
- Muestra concentración de viajes por área
- Porcentajes calculados automáticamente

### Cómo Usar Esta Pestaña

1. **Análisis Inicial**: Comienza aquí para entender el volumen general
2. **Identificar Patrones**: Usa el mapa de calor para encontrar tendencias
3. **Comparar Operadores**: Revisa la tabla de resumen
4. **Filtrar Datos**: Ajusta filtros en sidebar para análisis específicos

## 🕐 Pestaña Horas Pico

### Propósito
Analiza patrones de demanda por tiempo y ubicación para identificar horas y zonas de mayor actividad.

### Controles Principales

#### Selectores de Vista
```
┌─────────────────┬─────────────────┐
│ Ver por:        │ Agregar por:    │
│ • Hora del día  │ • Conteo viajes │
│ • Día semana    │ • Ingresos      │
│ • Zona          │ • Propinas      │
└─────────────────┴─────────────────┘
```

### Visualizaciones

#### 1. **Vista por Hora del Día**

**Mapa de Calor:**
- **Filas**: Horas (0-23)
- **Columnas**: Operadores
- **Intensidad**: Según métrica seleccionada

**Gráfico de Líneas:**
- Tendencia por hora
- Líneas por operador
- Marcadores en puntos de datos

**Interpretación:**
- **Horas Pico**: Generalmente 7-9 AM y 5-7 PM
- **Horas Valle**: Madrugada (2-5 AM)
- **Diferencias por Operador**: Algunos pueden dominar ciertas horas

#### 2. **Vista por Día de la Semana**

**Mapa de Calor:**
- **Filas**: Días (Lunes a Domingo)
- **Columnas**: Operadores

**Patrones Típicos:**
- **Lunes-Viernes**: Mayor actividad en horas laborales
- **Sábado-Domingo**: Picos diferentes, más actividad nocturna
- **Viernes**: Transición entre patrones laborales y de fin de semana

#### 3. **Vista por Zona**

**Análisis Geográfico:**
- Top zonas por actividad
- Distribución por operador
- Concentración de demanda

### Casos de Uso

1. **Planificación Operativa**: Identificar cuándo y dónde posicionar vehículos
2. **Análisis de Competencia**: Ver dominancia por horario
3. **Optimización de Precios**: Entender demanda para pricing dinámico
4. **Estudios de Movilidad**: Patrones de transporte urbano

## 🗺️ Pestaña Mapas

### Propósito
Visualización geoespacial de datos de viajes con mapas interactivos 2D y 3D.

### Tipos de Mapas

#### 1. **Mapa de Densidad (Folium)**

**Características:**
- Mapa base de OpenStreetMap
- Puntos de calor por concentración
- Zoom y pan interactivos
- Capas por operador

**Controles:**
- Selector de operador
- Tipo de visualización (pickup/dropoff)
- Nivel de agregación

#### 2. **Mapa 3D (PyDeck)**

**Visualizaciones Disponibles:**

**HexagonLayer:**
```python
# Configuración típica
layer = pdk.Layer(
    'HexagonLayer',
    data=data,
    get_position='[longitude, latitude]',
    radius=200,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True
)
```

**ColumnLayer:**
- Torres 3D por volumen de viajes
- Altura proporcional a cantidad
- Colores por operador

**ScatterplotLayer:**
- Puntos individuales
- Tamaño por duración/distancia
- Útil para análisis detallado

### Controles Interactivos

#### Filtros Geográficos
- **Borough**: Manhattan, Brooklyn, Queens, Bronx, Staten Island
- **Zona Específica**: Selección múltiple
- **Radio de Búsqueda**: Para análisis de área

#### Configuración Visual
- **Paleta de Colores**: Diferentes esquemas
- **Transparencia**: Ajuste de opacidad
- **Escala de Elevación**: Para mapas 3D

### Interpretación de Mapas

#### Patrones Comunes
1. **Manhattan**: Alta densidad en Midtown y Financial District
2. **Aeropuertos**: Clusters visibles en JFK, LaGuardia, Newark
3. **Estaciones de Tren**: Penn Station, Grand Central
4. **Zonas Residenciales**: Patrones dispersos en outer boroughs

#### Análisis Temporal
- Cambiar filtros de hora para ver evolución
- Comparar días laborales vs. fines de semana
- Identificar eventos especiales

## 💼 Pestaña Uber vs Lyft

### Propósito
Análisis competitivo detallado entre los principales operadores de ride-hailing.

### Métricas de Comparación

#### 1. **Cuota de Mercado**

**Gráfico Circular:**
- Distribución porcentual de viajes
- Colores corporativos (Uber: azul, Lyft: rosa)
- Valores absolutos y porcentajes

**Interpretación:**
- Dominancia general del mercado
- Variaciones por período
- Tendencias de crecimiento

#### 2. **Análisis de Ingresos**

**Métricas Incluidas:**
- Ingresos totales por empresa
- Ingreso promedio por viaje
- Distribución de propinas
- Eficiencia de pricing

**Visualizaciones:**
- Gráficos de barras comparativos
- Tendencias temporales
- Distribución de tarifas (boxplots)

#### 3. **Eficiencia Operativa**

**Métricas Calculadas:**
```python
# Precio por milla
price_per_mile = total_revenue / total_miles

# Precio por minuto
price_per_minute = total_revenue / (total_time / 60)

# Velocidad promedio
avg_speed = total_miles / (total_time / 60)
```

**Tabla de Eficiencia:**
| Empresa | Precio/Milla | Precio/Minuto | Velocidad Promedio |
|---------|--------------|---------------|--------------------|
| Uber    | $2.45/mi     | $0.85/min     | 12.3 mi/min       |
| Lyft    | $2.52/mi     | $0.88/min     | 11.8 mi/min       |

#### 4. **Concentración por Zonas**

**Top N Zonas:**
- Selector de número de zonas (5-15)
- Gráfico de barras agrupadas
- Análisis de dominancia por área

**Mapa de Calor de Dominancia:**
- Porcentaje de mercado por zona
- Escala de colores corporativos
- Identificación de fortalezas territoriales

#### 5. **Patrones Temporales**

**Por Hora del Día:**
- Gráfico de líneas comparativo
- Identificación de horas de dominancia
- Análisis de estrategias temporales

**Evolución de Cuota:**
- Gráfico de área apilada
- Muestra cambios en participación
- Tendencias de crecimiento/declive

#### 6. **Análisis de Aeropuertos**

**Participación Aeroportuaria:**
- Viajes hacia aeropuertos
- Viajes desde aeropuertos
- Comparación de tarifas aeroportuarias

### Insights Típicos

1. **Dominancia General**: Uber típicamente tiene mayor cuota
2. **Diferenciación Temporal**: Lyft puede dominar ciertos horarios
3. **Especialización Geográfica**: Fortalezas en diferentes zonas
4. **Estrategias de Pricing**: Diferencias en estructura tarifaria

## 💰 Pestaña Ingresos

### Propósito
Análisis detallado de la estructura de ingresos, tarifas, impuestos y propinas.

### Componentes de Ingresos

#### Estructura Tarifaria
```
Tarifa Total = Base Fare + Tolls + BCF + Sales Tax + 
               Congestion Surcharge + Airport Fee + Tips
```

#### Definiciones
- **Base Passenger Fare**: Tarifa base del viaje
- **Tolls**: Peajes de túneles y puentes
- **BCF**: Black Car Fund (fondo de seguro)
- **Sales Tax**: Impuesto de ventas
- **Congestion Surcharge**: Recargo por congestión (Manhattan)
- **Airport Fee**: Tarifa aeroportuaria
- **Tips**: Propinas del pasajero
- **Driver Pay**: Pago final al conductor

### Visualizaciones

#### 1. **Totales por Concepto**

**Tarjetas de Métricas:**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Pago        │ Propinas    │ Tarifa Base │ Impuestos   │
│ Conductor   │             │             │             │
│ $1,234,567  │ $234,567    │ $987,654    │ $123,456    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### 2. **Composición de Ingresos**

**Gráfico Circular:**
- Distribución porcentual de cada componente
- Colores diferenciados por tipo
- Valores absolutos en hover

#### 3. **Análisis por Empresa**

**Gráfico de Barras Apiladas:**
- Comparación de estructura tarifaria
- Identificación de diferencias estratégicas
- Análisis de competitividad

#### 4. **Tendencias Temporales**

**Evolución de Ingresos:**
- Gráfico de líneas por día
- Separado por empresa
- Identificación de tendencias

#### 5. **Análisis de Propinas**

**Métricas de Propinas:**
- Propina promedio por viaje
- Porcentaje de propina sobre tarifa
- Distribución de propinas
- Factores que influyen en propinas

**Correlaciones:**
- Propina vs. distancia
- Propina vs. duración
- Propina vs. hora del día
- Propina vs. zona

### Casos de Uso

1. **Análisis Financiero**: Entender estructura de costos
2. **Optimización Fiscal**: Análisis de impuestos y recargos
3. **Estrategia de Propinas**: Factores que aumentan propinas
4. **Benchmarking**: Comparación entre operadores

## ♿ Pestaña Accesibilidad

### Propósito
Análisis de servicios de accesibilidad, específicamente vehículos adaptados para sillas de ruedas (WAV - Wheelchair Accessible Vehicles).

### Métricas de Accesibilidad

#### Indicadores Principales
- **WAV Request**: Solicitudes de vehículos accesibles
- **WAV Match**: Coincidencias exitosas
- **Access-a-Ride**: Servicios de transporte accesible
- **Tasa de Cumplimiento**: % de solicitudes atendidas

### Análisis Disponibles

#### 1. **Volumen de Servicios**

**KPIs Principales:**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Solicitudes │ Atendidas   │ Tasa        │ Tiempo      │
│ WAV         │ WAV         │ Éxito       │ Promedio    │
│ 1,234       │ 1,156       │ 93.7%       │ 8.5 min     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### 2. **Distribución Geográfica**

**Mapa de Servicios:**
- Concentración de solicitudes por zona
- Áreas con mayor demanda
- Cobertura de servicios

**Análisis por Borough:**
- Distribución de servicios accesibles
- Identificación de gaps de servicio
- Oportunidades de mejora

#### 3. **Patrones Temporales**

**Por Hora del Día:**
- Demanda de servicios accesibles
- Comparación con servicios regulares
- Identificación de horas críticas

**Por Día de la Semana:**
- Variaciones en demanda
- Patrones de uso médico vs. recreativo

#### 4. **Análisis de Tarifas**

**Comparación Tarifaria:**
- WAV vs. servicios regulares
- Sobrecostos por accesibilidad
- Análisis de equidad tarifaria

#### 5. **Calidad del Servicio**

**Métricas de Rendimiento:**
- Tiempo de espera promedio
- Tasa de cancelación
- Satisfacción del usuario (si disponible)

### Insights para Accesibilidad

1. **Gaps de Servicio**: Zonas con baja cobertura
2. **Horas Críticas**: Momentos de alta demanda
3. **Eficiencia Operativa**: Optimización de flota WAV
4. **Equidad Tarifaria**: Análisis de costos adicionales

## ✈️ Pestaña Aeropuertos

### Propósito
Análisis especializado de conectividad aeroportuaria con los tres aeropuertos principales de NYC.

### Aeropuertos Incluidos

| Aeropuerto | Código | Zone ID | Ubicación |
|------------|--------|---------|----------|
| John F. Kennedy | JFK | 132 | Queens |
| LaGuardia | LGA | 138 | Queens |
| Newark Liberty | EWR | 1 | New Jersey |

### Análisis Disponibles

#### 1. **Viajes Hacia Aeropuertos**

**Métricas Principales:**
- Volumen total de viajes
- Distribución por aeropuerto
- Patrones horarios
- Zonas de origen más comunes

**Visualizaciones:**
- Gráfico de barras por aeropuerto
- Mapa de calor temporal
- Distribución geográfica de orígenes

#### 2. **Viajes Desde Aeropuertos**

**Análisis de Llegadas:**
- Destinos más populares
- Distribución temporal
- Comparación entre aeropuertos

**Patrones de Llegada:**
- Correlación con horarios de vuelos
- Picos de demanda
- Distribución por día de semana

#### 3. **Análisis Combinado**

**Comparación Direccional:**
```
┌─────────────────┬─────────┬─────────┬─────────┐
│ Dirección       │ Viajes  │ %Total  │ Tarifa  │
├─────────────────┼─────────┼─────────┼─────────┤
│ Hacia Aeropuerto│ 12,345  │ 8.5%    │ $45.67  │
│ Desde Aeropuerto│ 11,234  │ 7.8%    │ $42.34  │
│ No Aeropuerto   │ 120,456 │ 83.7%   │ $18.92  │
└─────────────────┴─────────┴─────────┴─────────┘
```

#### 4. **Análisis Tarifario**

**Estructura de Precios:**
- Tarifas base más altas
- Airport fees adicionales
- Comparación con viajes regulares

**Distribución de Tarifas:**
- Boxplots por aeropuerto
- Análisis de outliers
- Factores que afectan precio

#### 5. **Patrones Temporales**

**Por Hora del Día:**
- Picos matutinos (6-9 AM)
- Picos vespertinos (4-7 PM)
- Actividad nocturna reducida

**Por Día de la Semana:**
- Mayor actividad en días laborales
- Patrones de viajes de negocios
- Actividad de fin de semana

#### 6. **Competencia por Aeropuerto**

**Cuota de Mercado:**
- Uber vs. Lyft por aeropuerto
- Especialización por ubicación
- Estrategias competitivas

### Insights Aeroportuarios

1. **JFK**: Mayor volumen, viajes más largos
2. **LaGuardia**: Más conveniente desde Manhattan
3. **Newark**: Competencia con transporte público
4. **Pricing Premium**: 2-3x tarifa regular
5. **Horarios Críticos**: Correlación con vuelos

## 🤖 Pestaña Modelos ML

### Propósito
Interacción con modelos de machine learning para predicciones y análisis avanzado.

### Modelos Disponibles

#### 1. **Predictor de Tarifas**

**Objetivo**: Estimar el costo de un viaje (`driver_pay`)

**Características de Entrada:**
- Distancia del viaje (millas)
- Duración del viaje (minutos)
- Hora de recogida (0-23)
- Empresa (Uber, Lyft, etc.)
- Viaje hacia/desde aeropuerto
- Día de la semana

**Formulario Interactivo:**
```
┌─────────────────────────────────────────────┐
│ Predicción de Tarifa                        │
├─────────────────┬───────────────────────────┤
│ Distancia (mi): │ [5.0    ] ←→              │
│ Duración (min): │ [15     ] ←→              │
│ Hora recogida:  │ [12     ] ←→              │
│ Empresa:        │ [Uber   ▼]                │
│ □ Hacia aerop.  │ □ Desde aerop.            │
│                 │ [Predecir Tarifa]         │
└─────────────────┴───────────────────────────┘
```

**Resultado:**
- Tarifa estimada en dólares
- Medidor visual de confianza
- Rango de predicción

#### 2. **Clasificador de Aeropuertos**

**Objetivo**: Determinar si un viaje es hacia/desde aeropuerto

**Características de Entrada:**
- Distancia del viaje
- Duración del viaje
- Hora de recogida
- Empresa

**Resultado:**
- Clasificación binaria (Sí/No)
- Probabilidad de confianza
- Medidor visual de certeza

#### 3. **Análisis de Características**

**Feature Importance:**
- Ranking de variables más importantes
- Gráfico de barras horizontal
- Interpretación de resultados

**Ejemplo de Importancia:**
```
Distancia del viaje     ████████████████████ 45%
Duración del viaje      ████████████████     35%
Hora de recogida        ████████             15%
Empresa                 ████                  5%
```

### Métricas de Rendimiento

#### Predictor de Tarifas
- **RMSE**: < $3.00 (error promedio)
- **R²**: > 0.85 (varianza explicada)
- **MAE**: < $2.00 (error absoluto medio)

#### Clasificador de Aeropuertos
- **Accuracy**: > 92%
- **Precision**: > 90%
- **Recall**: > 88%
- **F1-Score**: > 89%

### Interpretación de Resultados

#### Predicción de Tarifas

**Factores que Aumentan Tarifa:**
- Mayor distancia
- Mayor duración
- Viajes aeroportuarios
- Horas pico
- Zonas premium

**Factores que Reducen Tarifa:**
- Viajes cortos
- Horas valle
- Zonas residenciales
- Promociones (no capturadas en modelo)

#### Clasificación de Aeropuertos

**Indicadores de Viaje Aeroportuario:**
- Distancia > 10 millas
- Duración > 25 minutos
- Horas típicas de vuelos
- Zonas de origen específicas

### Limitaciones de los Modelos

1. **Datos de Entrenamiento**: Basados en muestra del 5%
2. **Factores Externos**: No incluye tráfico en tiempo real
3. **Promociones**: No captura descuentos dinámicos
4. **Eventos Especiales**: No considera eventos que afectan demanda
5. **Actualización**: Modelos requieren reentrenamiento periódico

## 🎛️ Filtros y Personalización

### Filtros Disponibles

#### 1. **Filtro Temporal**

**Selección de Mes:**
- Dropdown con meses disponibles
- Formato: "2024 - MM"
- Carga automática de datos

**Rango de Horas:**
- Slider dual (0-23)
- Filtro en tiempo real
- Útil para análisis de horas específicas

#### 2. **Filtro de Operadores**

**Selección Múltiple:**
- Checkboxes para cada operador
- Uber, Lyft, Via, Juno (según disponibilidad)
- Selección/deselección masiva

#### 3. **Filtro Geográfico**

**Por Distrito (Borough):**
- Manhattan, Brooklyn, Queens, Bronx, Staten Island
- Selección múltiple
- Afecta zona de recogida

**Por Zona Específica:**
- Lista de zonas individuales
- Búsqueda por nombre
- Selección múltiple avanzada

#### 4. **Filtros Especiales**

**Solo Aeropuertos:**
- Checkbox para viajes aeroportuarios
- Incluye hacia Y desde aeropuertos
- Útil para análisis especializado

**Servicios de Accesibilidad:**
- Filtro por WAV requests
- Solo viajes accesibles
- Análisis de inclusión

### Comportamiento de Filtros

#### Aplicación en Tiempo Real
- Cambios se aplican inmediatamente
- Recálculo automático de métricas
- Actualización de visualizaciones

#### Persistencia
- Filtros se mantienen entre pestañas
- Reset manual disponible
- Estado guardado durante sesión

#### Combinación de Filtros
- Operación AND entre filtros
- Validación de datos resultantes
- Advertencia si no hay datos

### Consejos de Filtrado

1. **Análisis Específico**: Usa múltiples filtros para análisis detallado
2. **Comparaciones**: Cambia un filtro a la vez para comparar
3. **Rendimiento**: Menos datos = carga más rápida
4. **Validación**: Verifica que hay datos suficientes

## 📤 Exportación de Datos

### Opciones de Exportación

#### 1. **Gráficos**

**Plotly Charts:**
- Botón de descarga en cada gráfico
- Formatos: PNG, SVG, PDF
- Resolución configurable
- Incluye datos subyacentes

**Mapas:**
- Screenshot manual
- Exportación de coordenadas
- Datos de capas

#### 2. **Datos Procesados**

**Tablas Mostradas:**
- CSV download directo
- Datos filtrados actuales
- Formato compatible con Excel

**Datasets Completos:**
- Acceso a datos raw
- Formato Parquet original
- Documentación incluida

#### 3. **Reportes**

**Resumen Ejecutivo:**
- PDF con KPIs principales
- Gráficos embebidos
- Interpretación automática

**Análisis Detallado:**
- Reporte completo
- Todas las visualizaciones
- Metodología incluida

### Proceso de Exportación

1. **Seleccionar Datos**: Aplicar filtros deseados
2. **Elegir Formato**: PNG, CSV, PDF según necesidad
3. **Configurar Opciones**: Resolución, rango de datos
4. **Descargar**: Archivo se guarda localmente

## 💡 Consejos y Trucos

### Optimización de Rendimiento

#### 1. **Carga de Datos**
- Usa filtros para reducir dataset
- Selecciona meses específicos
- Evita cargar todos los operadores si no es necesario

#### 2. **Navegación Eficiente**
- Los filtros se mantienen entre pestañas
- Usa "Reset" para limpiar filtros
- Bookmark configuraciones útiles

#### 3. **Análisis Progresivo**
- Comienza con vista general (Resumen)
- Profundiza en áreas de interés
- Usa ML para validar hipótesis

### Interpretación de Datos

#### 1. **Contexto Temporal**
- Considera eventos especiales (feriados, clima)
- Compara períodos similares
- Identifica tendencias vs. anomalías

#### 2. **Validación Cruzada**
- Verifica insights en múltiples pestañas
- Usa diferentes visualizaciones
- Compara con datos externos

#### 3. **Limitaciones de Datos**
- Muestra del 5% puede tener sesgos
- Datos históricos vs. tiempo real
- Factores no capturados en dataset

### Casos de Uso Comunes

#### 1. **Análisis de Mercado**
```
1. Resumen → KPIs generales
2. Uber vs Lyft → Competencia
3. Mapas → Distribución geográfica
4. Horas Pico → Oportunidades temporales
```

#### 2. **Optimización Operativa**
```
1. Horas Pico → Identificar demanda
2. Mapas → Posicionamiento de flota
3. Aeropuertos → Rutas premium
4. ML → Predicción de demanda
```

#### 3. **Investigación Académica**
```
1. Resumen → Estadísticas descriptivas
2. Accesibilidad → Equidad de transporte
3. Ingresos → Estructura económica
4. Mapas → Patrones urbanos
```

### Solución de Problemas Comunes

#### 1. **"No hay datos para los filtros seleccionados"**
- Amplía rango de fechas
- Reduce número de filtros
- Verifica disponibilidad de datos

#### 2. **Gráficos no cargan**
- Refresca la página
- Verifica conexión a internet
- Reduce tamaño de dataset

#### 3. **Predicciones ML no funcionan**
- Verifica que modelos estén entrenados
- Revisa valores de entrada
- Consulta logs de error

#### 4. **Rendimiento lento**
- Usa menos filtros simultáneos
- Selecciona períodos más cortos
- Cierra otras pestañas del navegador

---

<div align="center">
  <strong>📖 ¡Domina el análisis de datos de transporte urbano! 📖</strong>
</div>