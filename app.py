import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
import pydeck as pdk
from datetime import datetime
import lightgbm as lgb
import warnings

# Configuración para eliminar warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
pd.options.mode.chained_assignment = None

# Configuración de página con tema profesional
st.set_page_config(
    page_title="🚖 NYC Ride-Hailing Analytics",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "NYC Ride-Hailing Analytics Dashboard - Professional Data Analysis Tool"
    }
)

# 🎨 CSS Personalizado con Paleta de Colores Profesional
st.markdown("""
<style>
    /* Paleta de Colores Definida */
    :root {
        --bg-primary: #1E1E2F;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0C3;
        --accent-blue: #4F9DFF;
        --accent-green: #4CAF50;
        --accent-red: #E53935;
        --card-bg: #2A2A3E;
        --border-color: #3A3A4E;
    }
    
    /* Fondo Principal */
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .main {
        padding-top: 2rem;
        background-color: var(--bg-primary) !important;
    }
    
    /* Sidebar Oscuro */
    .css-1d391kg {
        background-color: var(--card-bg) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Textos del Sidebar */
    .css-1d391kg .stMarkdown, 
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stMultiSelect label,
    .css-1d391kg .stSlider label,
    .css-1d391kg .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    /* Header personalizado */
    .header-container {
        background: linear-gradient(135deg, var(--accent-blue), #6B73FF);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(79, 157, 255, 0.3);
        text-align: center;
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Métricas Unificadas - Estilo Base Consistente */
    .metric-container {
        background: linear-gradient(135deg, var(--card-bg) 0%, rgba(42, 42, 62, 0.8) 100%);
        padding: 1.8rem;
        border-radius: 15px;
        border: 2px solid var(--border-color);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        margin: 0.8rem 0;
        transition: all 0.3s ease;
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-blue), #6B73FF);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        border-color: var(--accent-blue);
    }
    
    /* Métricas de Ingresos - Verde */
    .metric-income::before {
        background: linear-gradient(90deg, var(--accent-green), #66BB6A) !important;
    }
    
    .metric-income:hover {
        border-color: var(--accent-green) !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3) !important;
    }
    
    .metric-income .metric-value {
        color: var(--accent-green) !important;
        font-size: 2.2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Métricas de Viajes - Azul */
    .metric-trips .metric-value {
        color: var(--accent-blue) !important;
        font-size: 2.2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Métricas de Tiempo - Gris */
    .metric-time::before {
        background: linear-gradient(90deg, var(--text-secondary), #C0C0D3) !important;
    }
    
    .metric-time:hover {
        border-color: var(--text-secondary) !important;
        box-shadow: 0 10px 30px rgba(176, 176, 195, 0.3) !important;
    }
    
    .metric-time .metric-value {
        color: var(--text-secondary) !important;
        font-size: 2.2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    

    
    /* Tabs Estilizados */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--card-bg);
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        height: 50px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-blue) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(79, 157, 255, 0.4);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), #6B73FF);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 157, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 157, 255, 0.4);
    }
    
    /* Selectboxes y Controles */
    .stSelectbox > div > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stMultiSelect > div > div {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background-color: var(--accent-blue);
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: var(--card-bg);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    /* Gráficos */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    /* Alertas y Mensajes */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1) !important;
        border: 1px solid var(--accent-green) !important;
        color: var(--accent-green) !important;
        border-radius: 10px;
    }
    
    .stInfo {
        background-color: rgba(79, 157, 255, 0.1) !important;
        border: 1px solid var(--accent-blue) !important;
        color: var(--accent-blue) !important;
        border-radius: 10px;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid #FFC107 !important;
        color: #FFC107 !important;
        border-radius: 10px;
    }
    
    .stError {
        background-color: rgba(229, 57, 53, 0.1) !important;
        border: 1px solid var(--accent-red) !important;
        color: var(--accent-red) !important;
        border-radius: 10px;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Loading spinner personalizado */
    .stSpinner {
        text-align: center;
    }
    
    /* Animaciones suaves */
    * {
        transition: all 0.3s ease;
    }
    
    /* Textos principales */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Textos secundarios */
    .stCaption {
        color: var(--text-secondary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header profesional
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚖 NYC Ride-Hailing Analytics</h1>
    <p class="header-subtitle">Professional Data Analysis Dashboard | Real-time Insights & Predictive Analytics</p>
</div>
""", unsafe_allow_html=True)

DATA_FOLDER = "data_sampled"
REQUIRED_COLS = ["pickup_datetime", "hvfhs_license_num", "PULocationID", "DOLocationID", "tips", "driver_pay"]

# Configuración de datos con caching
@st.cache_data
def load_zone_data():
    """Carga datos de zonas con caching para mejor rendimiento"""
    try:
        zones_df = pd.read_csv("data/taxi_zone_lookup.csv")
        # Aeropuertos: JFK (132), LaGuardia (138), Newark EWR (1)
        airport_zones = [1, 132, 138]
        airport_names = {1: "Newark (EWR)", 132: "JFK", 138: "LaGuardia (LGA)"}
        
        # Cargar coordenadas de centroides para zonas
        try:
            centroids_df = pd.read_csv("data/taxi_zone_centroids.csv")
            # Combinar datos de zonas con coordenadas
            zones_with_coords = zones_df.merge(centroids_df, on="LocationID", how="left")
            return zones_df, zones_with_coords, airport_zones, airport_names, True
        except Exception:
            return zones_df, zones_df, airport_zones, airport_names, False
    except Exception:
        return None, None, [], {}, False

# Cargar datos de zonas
zones_df, zones_with_coords, AIRPORT_ZONES, AIRPORT_NAMES, coords_loaded = load_zone_data()

# Mostrar estado de carga solo en modo debug
if st.sidebar.checkbox("🔧 Modo Debug", value=False):
    if zones_df is not None:
        if coords_loaded:
            st.sidebar.success("✅ Datos de zonas y coordenadas cargados")
        else:
            st.sidebar.info("ℹ️ Zonas cargadas, coordenadas no disponibles")
    else:
        st.sidebar.warning("⚠️ Datos de zonas no disponibles")

# Carga optimizada de archivos con caching
@st.cache_data
def get_available_files():
    """Obtiene lista de archivos disponibles con caching"""
    files = sorted(glob.glob(f"{DATA_FOLDER}/*_reduced.parquet"))
    months = [os.path.basename(f).replace("_reduced.parquet", "") for f in files]
    return dict(zip(months, files)), months

file_map, months = get_available_files()

# Sidebar profesional con filtros
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, var(--accent-blue), #6B73FF); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; 
                box-shadow: 0 4px 12px rgba(79, 157, 255, 0.3);">
        <h2 style="color: white; margin: 0; text-align: center; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">🔍 Filtros de Análisis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de mes con mejor diseño
    selected_month = st.selectbox(
        "📅 Período de Análisis:", 
        months,
        help="Selecciona el mes para analizar los datos de viajes"
    )
    
    # Información profesional
    st.markdown("""
    <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px; 
                border-left: 4px solid var(--accent-green); margin: 1rem 0;
                border: 1px solid var(--border-color);">
        <small style="color: var(--text-primary);"><strong>📊 Dataset:</strong> Muestra representativa del 5% de viajes por operador</small>
    </div>
    """, unsafe_allow_html=True)

# Carga y procesamiento optimizado de datos
@st.cache_data
def load_and_process_data(file_path):
    """Carga y procesa datos con caching para mejor rendimiento"""
    try:
        # Cargar datos
        df = pd.read_parquet(file_path)
        
        # Validar columnas requeridas
        missing = [col for col in REQUIRED_COLS if col not in df.columns]
        if missing:
            return None, f"Faltan columnas requeridas: {', '.join(missing)}"
        
        # Procesar columnas de tiempo
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
        
        # Crear características temporales si no existen
        if "pickup_hour" not in df.columns:
            df["pickup_hour"] = df["pickup_datetime"].dt.hour
        if "pickup_weekday" not in df.columns:
            df["pickup_weekday"] = df["pickup_datetime"].dt.weekday
        if "pickup_month" not in df.columns:
            df["pickup_month"] = df["pickup_datetime"].dt.month
        
        # Añadir nombres de días
        days_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 
                   4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df["day_name"] = df["pickup_weekday"].map(days_map)
        
        return df, None
        
    except Exception as e:
        return None, f"Error al cargar datos: {str(e)}"

# Cargar datos del mes seleccionado
with st.spinner("🔄 Cargando y procesando datos..."):
    file_path = file_map[selected_month]
    df, error_msg = load_and_process_data(file_path)
    
    if df is None:
        st.error(f"❌ {error_msg}")
        st.stop()
    
    # Mostrar información del dataset en modo debug
    if st.sidebar.checkbox("📊 Info Dataset", value=False):
        st.sidebar.success(f"✅ Dataset cargado: {len(df):,} registros")
        st.sidebar.info(f"📅 Período: {selected_month}")

# Unir con zonas si existen
if zones_df is not None:
    df = df.merge(zones_df, left_on="PULocationID", right_on="LocationID", how="left")
    df.rename(columns={"Zone": "pickup_zone", "Borough": "pickup_borough"}, inplace=True)
    
    # Merge para zonas de destino
    df = df.merge(zones_df, left_on="DOLocationID", right_on="LocationID", how="left", suffixes=("", "_dropoff"))
    df.rename(columns={"Zone": "dropoff_zone", "Borough": "dropoff_borough"}, inplace=True)
    
    # Asegurarse de que no haya columnas duplicadas
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Marcar viajes desde/hacia aeropuertos
    df["from_airport"] = df["PULocationID"].isin(AIRPORT_ZONES)
    df["to_airport"] = df["DOLocationID"].isin(AIRPORT_ZONES)

# Filtros disponibles
operadores = df["hvfhs_license_num"].dropna().unique()
# Usar una forma más explícita para obtener valores únicos
if "pickup_zone" in df.columns:
    pickup_zones = df["pickup_zone"].dropna()
    zonas_disponibles = sorted(list(set(pickup_zones)))
else:
    zonas_disponibles = []
    
if "pickup_borough" in df.columns:
    pickup_boroughs = df["pickup_borough"].dropna()
    boroughs = sorted(list(set(pickup_boroughs)))
else:
    boroughs = []

with st.sidebar:
    # Separador visual
    st.markdown("---")
    
    # Filtros de operadores con mejor diseño
    st.markdown("**🏢 Operadores de Transporte**")
    selected_ops = st.multiselect(
        "Selecciona operadores:", 
        operadores, 
        default=list(operadores),
        help="Filtra por empresas de ride-hailing"
    )
    
    # Filtro de horas con mejor diseño
    st.markdown("**🕐 Rango Horario**")
    selected_hours = st.slider(
        "Horas de operación:", 
        0, 23, (0, 23),
        help="Selecciona el rango de horas para analizar"
    )
    
    # Filtro por distrito con validación
    if len(boroughs) > 0:
        st.markdown("**📍 Distritos de NYC**")
        selected_boroughs = st.multiselect(
            "Selecciona distritos:", 
            boroughs, 
            default=list(boroughs),
            help="Filtra por borough de recogida"
        )
        borough_filter = df["pickup_borough"].isin(selected_boroughs) if selected_boroughs else pd.Series([True] * len(df))
    else:
        borough_filter = pd.Series([True] * len(df))
    
    # Filtro de aeropuertos con mejor diseño
    st.markdown("**✈️ Filtros Especiales**")
    show_airport_only = st.checkbox(
        "Solo viajes aeroportuarios", 
        value=False,
        help="Mostrar únicamente viajes hacia/desde aeropuertos"
    )
    
    if show_airport_only and "from_airport" in df.columns and "to_airport" in df.columns:
        airport_filter = (df["from_airport"] | df["to_airport"])
    else:
        airport_filter = pd.Series([True] * len(df))

# Aplicar filtros de manera optimizada
@st.cache_data
def apply_filters(df, selected_ops, selected_hours, borough_filter, airport_filter):
    """Aplica filtros de manera optimizada con caching"""
    try:
        # Crear máscara de filtros
        mask = (
            df["hvfhs_license_num"].isin(selected_ops) &
            df["pickup_hour"].between(selected_hours[0], selected_hours[1]) &
            borough_filter &
            airport_filter
        )
        return df[mask]
    except Exception:
        return df  # Retornar datos sin filtrar en caso de error

# Aplicar filtros
df_filtered = apply_filters(df, selected_ops, selected_hours, borough_filter, airport_filter)

# Validación de datos filtrados
if len(df_filtered) == 0:
    st.markdown("""
    <div style="background: #fff3cd; border: 1px solid #ffeaa7; 
                border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: #856404; margin: 0;">⚠️ Sin Datos Disponibles</h4>
        <p style="color: #856404; margin: 0.5rem 0 0 0;">No hay datos que coincidan con los filtros seleccionados. 
        Intenta ampliar los criterios de búsqueda.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Mostrar estadísticas de filtrado en sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("**📈 Estadísticas del Filtro**")
    total_records = len(df)
    filtered_records = len(df_filtered)
    filter_percentage = (filtered_records / total_records) * 100 if total_records > 0 else 0
    
    st.metric(
        "Registros mostrados", 
        f"{filtered_records:,}",
        f"{filter_percentage:.1f}% del total"
    )
    
    if filtered_records < total_records:
        st.info(f"🔍 Filtrado: {total_records - filtered_records:,} registros ocultos")

# Tabs principales
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Resumen", 
    "🕐 Horas Pico", 
    "🗺️ Mapas", 
    "💼 Uber vs Lyft",
    "💰 Ingresos", 
    "✈️ Aeropuertos",
    "🤖 Modelos ML"
])

with tab1:
    st.subheader("Resumen general")
    
    # KPIs principales con colores consistentes
    col1, col2, col3, col4 = st.columns(4)
    total_trips = len(df_filtered)
    unique_days = df_filtered["pickup_datetime"].dt.date.nunique()
    
    # Métrica de Viajes - Azul
    col1.markdown(f"""
    <div class="metric-container metric-trips">
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">🧾 Viajes</div>
        <div class="metric-value">{total_trips:,}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métrica de Días - Tiempo (Gris)
    col2.markdown(f"""
    <div class="metric-container metric-time">
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">📅 Días únicos</div>
        <div class="metric-value">{unique_days}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métrica de Operadores - Azul
    col3.markdown(f"""
    <div class="metric-container metric-trips">
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">🏢 Operadores</div>
        <div class="metric-value">{df_filtered["hvfhs_license_num"].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ingresos totales - Verde
    if "driver_pay" in df_filtered.columns:
        total_pay = df_filtered["driver_pay"].sum()
        col4.markdown(f"""
        <div class="metric-container metric-income">
            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">💲 Ingresos Totales</div>
            <div class="metric-value">${total_pay:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sección de insights destacados
    st.subheader("🔍 Insights principales")
    insight_cols = st.columns(3)
    
    # 1. Promedio diario de viajes - Azul
    avg_daily_trips = total_trips / unique_days if unique_days > 0 else 0
    insight_cols[0].markdown(f"""
    <div class="metric-container metric-trips">
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">📊 Promedio diario de viajes</div>
        <div class="metric-value">{avg_daily_trips:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Distancia promedio - Tiempo (Gris)
    if "trip_miles" in df_filtered.columns:
        avg_miles = df_filtered["trip_miles"].mean()
        insight_cols[1].markdown(f"""
        <div class="metric-container metric-time">
            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">📏 Distancia promedio</div>
            <div class="metric-value">{avg_miles:.2f} mi</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3. Duración promedio - Tiempo (Gris)
    if "trip_time" in df_filtered.columns:
        avg_time_min = df_filtered["trip_time"].mean() / 60  # Convertir a minutos
        insight_cols[2].markdown(f"""
        <div class="metric-container metric-time">
            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">⏱️ Duración promedio</div>
            <div class="metric-value">{avg_time_min:.1f} min</div>
        </div>
        """, unsafe_allow_html=True)
    

    
    # Distribución por hora y día
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df_filtered, x="pickup_hour", color="hvfhs_license_num", barmode="group")
        fig1.update_layout(
            title="📈 Distribución de viajes por hora",
            xaxis_title="Hora del día",
            yaxis_title="Número de viajes"
        )
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        if "day_name" in df_filtered:
            order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            fig2 = px.histogram(df_filtered, x="day_name", color="hvfhs_license_num", barmode="group",
                                category_orders={"day_name": order})
        else:
            fig2 = px.histogram(df_filtered, x="pickup_weekday", color="hvfhs_license_num", barmode="group")
        fig2.update_layout(
            title="📅 Distribución por día de la semana",
            xaxis_title="Día de la semana",
            yaxis_title="Número de viajes"
        )
        st.plotly_chart(fig2, width='stretch')
    
    # Mapa de calor por hora y día
    st.subheader("🔥 Patrón de viajes por hora y día")
    
    # Crear pivot table para el mapa de calor
    if "day_name" in df_filtered.columns:
        day_col = "day_name"
        day_order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    else:
        day_col = "pickup_weekday"
        day_order = list(range(7))
        
    heatmap_data = df_filtered.groupby(["pickup_hour", day_col]).size().reset_index(name="trips")
    heatmap_pivot = heatmap_data.pivot(index="pickup_hour", columns=day_col, values="trips").fillna(0)
    
    if day_col == "day_name":
        # Reordenar las columnas para que los días estén en orden
        heatmap_pivot = heatmap_pivot[day_order]
    
    fig_heatmap = px.imshow(
        heatmap_pivot,
        color_continuous_scale="Viridis",
        labels=dict(x="Día de la semana", y="Hora del día", color="Número de viajes"),
        title="Mapa de calor: Viajes por hora y día"
    )
    fig_heatmap.update_layout(height=450)
    st.plotly_chart(fig_heatmap, width='stretch')
    
    # Gráfico de tendencia temporal (si hay suficientes días)
    if unique_days > 3:
        st.subheader("📈 Tendencia temporal")
        # Agrupar por fecha
        df_filtered["pickup_date"] = df_filtered["pickup_datetime"].dt.date
        daily_trend = df_filtered.groupby(["pickup_date", "hvfhs_license_num"]).size().reset_index(name="trips")
        
        fig_trend = px.line(
            daily_trend,
            x="pickup_date",
            y="trips",
            color="hvfhs_license_num",
            markers=True,
            title="Evolución diaria del número de viajes",
            labels={"pickup_date": "Fecha", "trips": "Número de viajes", "hvfhs_license_num": "Operador"}
        )
        st.plotly_chart(fig_trend, width='stretch')
    
    # Resumen por operador
    st.subheader("📊 Resumen por operador")
    op_summary = df_filtered.groupby("hvfhs_license_num").agg({
        "pickup_datetime": "count",
        "driver_pay": "sum",
        "tips": "sum"
    }).reset_index()
    op_summary.columns = ["Operador", "Viajes", "Ingresos", "Propinas"]
    op_summary["Propina Promedio"] = op_summary["Propinas"] / op_summary["Viajes"]
    op_summary["% Propina"] = (op_summary["Propinas"] / op_summary["Ingresos"]) * 100
    
    # Añadir métricas de distancia y duración si están disponibles
    if "trip_miles" in df_filtered.columns:
        op_summary["Distancia Promedio (millas)"] = df_filtered.groupby("hvfhs_license_num")["trip_miles"].mean().values
    
    if "trip_time" in df_filtered.columns:
        op_summary["Duración Promedio (min)"] = df_filtered.groupby("hvfhs_license_num")["trip_time"].mean().values / 60
    
    # Formatear valores monetarios y numéricos
    op_summary["Ingresos"] = op_summary["Ingresos"].apply(lambda x: f"${x:,.2f}")
    op_summary["Propinas"] = op_summary["Propinas"].apply(lambda x: f"${x:,.2f}")
    op_summary["Propina Promedio"] = op_summary["Propina Promedio"].apply(lambda x: f"${x:.2f}")
    op_summary["% Propina"] = op_summary["% Propina"].apply(lambda x: f"{x:.1f}%")
    
    if "Distancia Promedio (millas)" in op_summary.columns:
        op_summary["Distancia Promedio (millas)"] = op_summary["Distancia Promedio (millas)"].apply(lambda x: f"{x:.2f}")
    
    if "Duración Promedio (min)" in op_summary.columns:
        op_summary["Duración Promedio (min)"] = op_summary["Duración Promedio (min)"].apply(lambda x: f"{x:.1f}")
    
    st.dataframe(op_summary, width='stretch')
    
    # Distribución geográfica resumida (si hay datos de zonas)
    if "pickup_borough" in df_filtered.columns:
        st.subheader("🗺️ Distribución geográfica")
        
        # Agrupar por distrito (borough)
        borough_dist = df_filtered.groupby("pickup_borough").size().reset_index(name="trips")
        borough_dist = borough_dist.sort_values("trips", ascending=False)
        
        # Calcular porcentajes
        borough_dist["Porcentaje"] = (borough_dist["trips"] / borough_dist["trips"].sum()) * 100
        
        # Crear gráfica circular
        fig_geo = px.pie(
            borough_dist, 
            values="trips", 
            names="pickup_borough",
            title="Distribución de viajes por distrito",
            hover_data=["Porcentaje"],
            labels={"pickup_borough": "Distrito", "trips": "Viajes", "Porcentaje": "% del total"}
        )
        fig_geo.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_geo, width='stretch')
    
    st.dataframe(op_summary, width='stretch')

with tab2:
    st.subheader("🕐 Análisis de Horas Pico")
    
    # Selección de filtros específicos
    col1, col2 = st.columns(2)
    with col1:
        view_by = st.selectbox("Ver por:", ["Hora del día", "Día de la semana", "Zona"])
    with col2:
        agg_by = st.selectbox("Agregar por:", ["Conteo de viajes", "Ingresos", "Propinas"])
    
    # Preparar datos según las selecciones
    if agg_by == "Conteo de viajes":
        agg_func = "count"
        value_col = "pickup_datetime"
        title_prefix = "Cantidad de viajes"
    elif agg_by == "Ingresos":
        agg_func = "sum"
        value_col = "driver_pay"
        title_prefix = "Total de ingresos ($)"
    else:
        agg_func = "sum"
        value_col = "tips"
        title_prefix = "Total de propinas ($)"
    
    # Visualización según la vista seleccionada
    if view_by == "Hora del día":
        # Heatmap de horas del día por operador
        hour_data = df_filtered.pivot_table(
            index="pickup_hour",
            columns="hvfhs_license_num",
            values=value_col,
            aggfunc=agg_func
        ).fillna(0)
        
        fig = px.imshow(
            hour_data,
            color_continuous_scale="Viridis",
            labels=dict(x="Operador", y="Hora del día", color=title_prefix)
        )
        fig.update_layout(title=f"Mapa de calor: {title_prefix} por hora y operador")
        st.plotly_chart(fig, width='stretch')
        
        # Gráfica de línea por hora
        hour_summary = df_filtered.groupby(["pickup_hour", "hvfhs_license_num"]).agg({value_col: agg_func}).reset_index()
        fig2 = px.line(
            hour_summary, 
            x="pickup_hour", 
            y=value_col, 
            color="hvfhs_license_num",
            markers=True,
            title=f"{title_prefix} por hora del día"
        )
        st.plotly_chart(fig2, width='stretch')
        
    elif view_by == "Día de la semana":
        # Heatmap de días de la semana por operador
        if "day_name" in df_filtered.columns:
            weekday_data = df_filtered.pivot_table(
                index="day_name",
                columns="hvfhs_license_num",
                values=value_col,
                aggfunc=agg_func
            ).fillna(0)
            
            # Reordenar días
            order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            weekday_data = weekday_data.reindex(order)
        else:
            weekday_data = df_filtered.pivot_table(
                index="pickup_weekday",
                columns="hvfhs_license_num",
                values=value_col,
                aggfunc=agg_func
            ).fillna(0)
        
        fig = px.imshow(
            weekday_data,
            color_continuous_scale="Viridis",
            labels=dict(x="Operador", y="Día de la semana", color=title_prefix)
        )
        fig.update_layout(title=f"Mapa de calor: {title_prefix} por día de semana y operador")
        st.plotly_chart(fig, width='stretch')
        
    else:  # Por zonas
        if "pickup_zone" in df_filtered.columns:
            # Top 15 zonas
            top_zones = df_filtered.groupby("pickup_zone").size().nlargest(15).index
            zone_data = df_filtered[df_filtered["pickup_zone"].isin(top_zones)]
            
            zone_summary = zone_data.pivot_table(
                index="pickup_zone",
                columns="hvfhs_license_num",
                values=value_col,
                aggfunc=agg_func
            ).fillna(0)
            
            fig = px.imshow(
                zone_summary,
                color_continuous_scale="Viridis",
                labels=dict(x="Operador", y="Zona", color=title_prefix)
            )
            fig.update_layout(
                title=f"Mapa de calor: {title_prefix} por zona y operador (Top 15)",
                height=800
            )
            st.plotly_chart(fig, width='stretch')
            
            # Barras por zona
            zone_totals = zone_data.groupby(["pickup_zone", "hvfhs_license_num"]).agg({value_col: agg_func}).reset_index()
            fig2 = px.bar(
                zone_totals,
                x="pickup_zone",
                y=value_col,
                color="hvfhs_license_num",
                title=f"Top 15 zonas por {title_prefix.lower()}"
            )
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, width='stretch')
        else:
            st.warning("No hay datos de zonas disponibles para este análisis.")
    
    # Análisis de hot spots (combinación hora-día)
    st.subheader("🔥 Hot spots (Hora del día vs Día de la semana)")
    
    if "day_name" in df_filtered.columns:
        pivot_day = "day_name"
        category_orders = {"day_name": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
    else:
        pivot_day = "pickup_weekday"
        category_orders = None
    
    hotspot_data = df_filtered.pivot_table(
        index="pickup_hour",
        columns=pivot_day,
        values=value_col,
        aggfunc=agg_func
    ).fillna(0)
    
    fig = px.imshow(
        hotspot_data,
        color_continuous_scale="Viridis",
        labels=dict(x="Día de la semana", y="Hora del día", color=title_prefix)
    )
    fig.update_layout(title=f"Mapa de calor: {title_prefix} por hora y día")
    st.plotly_chart(fig, width='stretch')

with tab3:
    st.subheader("🗺️ Visualización Geoespacial")
    
    if "pickup_zone" not in df_filtered.columns or "pickup_borough" not in df_filtered.columns:
        st.warning("No hay datos geoespaciales disponibles. Asegúrate de que los datos incluyan columnas de zona y coordenadas.")
    else:
        map_type = st.radio("Tipo de visualización:", ["Heatmap de zonas", "Mapa de densidad"], horizontal=True)
        
        if map_type == "Heatmap de zonas":
            # Contar viajes por zona
            zone_counts = df_filtered.groupby(["pickup_zone", "pickup_borough"]).size().reset_index(name="trip_count")
            zone_counts = zone_counts.sort_values("trip_count", ascending=False)
            
            # Mostrar tabla de resultados
            st.dataframe(zone_counts, width='stretch')
            
            # Crear gráfico de barras para top zonas
            top_n = st.slider("Mostrar top N zonas:", 5, 30, 15)
            top_zones = zone_counts.head(top_n)
            
            fig = px.bar(
                top_zones, 
                x="pickup_zone", 
                y="trip_count", 
                color="pickup_borough",
                title=f"Top {top_n} Zonas con Mayor Número de Viajes",
                labels={"pickup_zone": "Zona", "trip_count": "Cantidad de Viajes", "pickup_borough": "Distrito"}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')
              # Crear mapa de burbujas si hay datos de coordenadas disponibles
            try:
                if zones_with_coords is not None and "Lat" in zones_with_coords.columns and "Lon" in zones_with_coords.columns:
                    # Crear mapa base
                    ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
                    
                    # Normalizar para el tamaño de círculos
                    max_count = zone_counts["trip_count"].max()
                    
                    # Añadir círculos para cada zona
                    for _, row in zone_counts.iterrows():
                        # Buscar las coordenadas de la zona
                        zone_info = zones_with_coords[zones_with_coords["Zone"] == row["pickup_zone"]]
                        if not zone_info.empty:
                            zone_info = zone_info.iloc[0]
                            # Verificar que las coordenadas sean válidas
                            if zone_info["Lat"] != 0 and zone_info["Lon"] != 0:
                                folium.Circle(
                                    location=[zone_info["Lat"], zone_info["Lon"]],
                                    radius=100 * (row["trip_count"] / max_count) * 2,  # Ajustar tamaño
                                    color='crimson',
                                    fill=True,
                                    fill_color='crimson',
                                    fill_opacity=0.6,
                                    tooltip=f"{row['pickup_zone']} ({row['pickup_borough']}): {row['trip_count']} viajes"
                                ).add_to(ny_map)
                    
                    st.subheader("Mapa de concentración de viajes por zona")
                    folium_static(ny_map)
                else:
                    st.info("No hay coordenadas disponibles para crear el mapa. Asegúrate de que el archivo de zonas incluya columnas Lat y Lon.")
            except Exception as e:
                st.error(f"Error al crear el mapa: {e}")
                st.exception(e)  # Mostrar detalles del error
        
        else:  # Mapa de densidad
            st.info("Preparando mapa de densidad...")
            
            # Verificar si tenemos datos de lat/lon
            if "pickup_latitude" in df_filtered.columns and "pickup_longitude" in df_filtered.columns:
                # Crear muestra si hay muchos datos
                if len(df_filtered) > 10000:
                    map_data = df_filtered.sample(10000)
                else:
                    map_data = df_filtered
                
                # Crear mapa PyDeck
                layer = pdk.Layer(
                    "HeatmapLayer",
                    data=map_data,
                    get_position=["pickup_longitude", "pickup_latitude"],
                    opacity=0.9,
                    get_weight="1",
                    threshold=0.05,
                    radius_pixels=50,
                )
                
                # Set the viewport
                view_state = pdk.ViewState(
                    longitude=-74.0060,
                    latitude=40.7128,
                    zoom=10,
                    min_zoom=5,
                    max_zoom=15,
                    pitch=0,
                    bearing=0
                )
                
                # Render
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=view_state,
                    layers=[layer],
                ))
            else:
                # Intentar usar centroides de zona si no hay datos lat/lon directos
                try:
                    if zones_with_coords is not None and "Lat" in zones_with_coords.columns and "Lon" in zones_with_coords.columns:
                        # Preparar datos para el mapa
                        pickup_counts = df_filtered.groupby("PULocationID").size().reset_index(name="count")
                        
                        # Unir con las coordenadas
                        map_data = pickup_counts.merge(zones_with_coords[["LocationID", "Lat", "Lon"]], 
                                                      left_on="PULocationID", 
                                                      right_on="LocationID", 
                                                      how="left")
                        
                        # Filtrar zonas sin coordenadas válidas
                        map_data = map_data[(map_data["Lat"] != 0) & (map_data["Lon"] != 0)]
                        
                        if not map_data.empty:
                            # Crear capa de mapa
                            layer = pdk.Layer(
                                "HeatmapLayer",
                                data=map_data,
                                get_position=["Lon", "Lat"],
                                opacity=0.9,
                                get_weight="count",
                                threshold=0.05,
                                radius_pixels=50,
                            )
                            
                            # Set the viewport
                            view_state = pdk.ViewState(
                                longitude=-74.0060,
                                latitude=40.7128,
                                zoom=10,
                                min_zoom=5,
                                max_zoom=15,
                                pitch=0,
                                bearing=0
                            )
                            
                            # Render
                            st.pydeck_chart(pdk.Deck(
                                map_style="mapbox://styles/mapbox/dark-v10",
                                initial_view_state=view_state,
                                layers=[layer],
                            ))
                        else:
                            st.warning("No hay suficientes datos con coordenadas válidas para crear el mapa de calor.")
                    else:
                        st.warning("No hay coordenadas disponibles para las zonas.")
                except Exception as e:
                    st.error(f"Error al crear el mapa de calor: {e}")
                    st.exception(e)  # Mostrar detalles del error
    
    # Mostrar flujos entre zonas
    st.subheader("🔄 Flujos de viajes entre zonas")
    if "pickup_zone" in df_filtered.columns and "dropoff_zone" in df_filtered.columns:
        # Calcular los flujos más comunes
        flows = df_filtered.groupby(["pickup_zone", "dropoff_zone"]).size().reset_index(name="trip_count")
        flows = flows.sort_values("trip_count", ascending=False)
        
        # Mostrar top flujos
        st.dataframe(flows.head(20), width='stretch')
        
        # Crear gráfico de sankey o red para top flujos
        top_flows = flows.head(15)
        fig = go.Figure(data=[go.Sankey(
            node=dict(
              pad=15,
              thickness=20,
              line=dict(color="black", width=0.5),
              label=list(set(top_flows["pickup_zone"].tolist() + top_flows["dropoff_zone"].tolist())),
            ),
            link=dict(
              source=[list(set(top_flows["pickup_zone"].tolist() + top_flows["dropoff_zone"].tolist())
                      ).index(x) for x in top_flows["pickup_zone"]],
              target=[list(set(top_flows["pickup_zone"].tolist() + top_flows["dropoff_zone"].tolist())
                      ).index(x) for x in top_flows["dropoff_zone"]],
              value=top_flows["trip_count"],
          ))])
        
        fig.update_layout(title_text="Top 15 Flujos de Viajes entre Zonas", font_size=12)
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("No hay suficiente información de zonas para mostrar flujos de viajes.")
        
with tab4:
    st.subheader("💼 Comparativa Uber vs Lyft")
    
    # Filtrar solo para Uber y Lyft
    uber_lyft = df_filtered[df_filtered["hvfhs_license_num"].isin(["Uber", "Lyft"])]
    
    if len(uber_lyft) == 0:
        st.warning("No hay datos de Uber o Lyft para comparar.")
    else:
        # Banner de información general
        st.info("Esta sección analiza las diferencias entre Uber y Lyft en términos de actividad, tarifas, propinas y patrones de viaje. Usa los filtros del panel izquierdo para ajustar el análisis.")
        
        # Análisis general con métricas clave destacadas
        col1, col2 = st.columns(2)
        
        # --- PRIMERA COLUMNA: DISTRIBUCIÓN DE VIAJES Y MÉTRICAS ---
        with col1:
            # Conteo de viajes por empresa
            trip_counts = uber_lyft["hvfhs_license_num"].value_counts().reset_index()
            trip_counts.columns = ["Empresa", "Cantidad de Viajes"]
            
            # Calculando la cuota de mercado como porcentaje
            total_trips = trip_counts["Cantidad de Viajes"].sum()
            trip_counts["Cuota de Mercado"] = (trip_counts["Cantidad de Viajes"] / total_trips * 100).round(1).astype(str) + '%'
            
            # Crear gráfica de pie mejorada
            fig = px.pie(
                trip_counts, 
                values="Cantidad de Viajes", 
                names="Empresa",
                title="<b>Distribución de Viajes por Empresa</b>",
                color="Empresa",
                color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
                hover_data=["Cuota de Mercado"]
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.03, 0.03])
            fig.update_layout(
                font_size=12,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, width='stretch')
            
            # Métricas detalladas en Uber vs Lyft
            st.subheader("⚖️ Comparativa de Métricas Principales")
            
            metrics_data = []
            
            # Recopilar todas las métricas disponibles
            metrics_to_calculate = {
                "driver_pay": {"name": "Tarifa Promedio", "format": "${:.2f}", "agg": "mean", "available": False},
                "tips": {"name": "Propina Promedio", "format": "${:.2f}", "agg": "mean", "available": False},
                "trip_miles": {"name": "Distancia Promedio", "format": "{:.2f} mi", "agg": "mean", "available": False},
                "trip_time": {"name": "Duración Promedio", "format": "{:.1f} min", "agg": "mean", "available": False, "divisor": 60},
                "pickup_datetime": {"name": "Viajes Totales", "format": "{:,.0f}", "agg": "count", "available": False},
            }
            
            # Verificar qué métricas están disponibles
            for col, config in metrics_to_calculate.items():
                if col in uber_lyft.columns:
                    metrics_to_calculate[col]["available"] = True
            
            # Calcular las métricas disponibles
            for operator in ["Uber", "Lyft"]:
                operator_data = {"Empresa": operator}
                operator_subset = uber_lyft[uber_lyft["hvfhs_license_num"] == operator]
                
                for col, config in metrics_to_calculate.items():
                    if config["available"]:
                        if config["agg"] == "mean":
                            if "divisor" in config:
                                value = operator_subset[col].mean() / config["divisor"]
                            else:
                                value = operator_subset[col].mean()
                        elif config["agg"] == "count":
                            value = len(operator_subset)
                        else:
                            value = operator_subset[col].sum()
                            
                        operator_data[config["name"]] = config["format"].format(value)
                
                metrics_data.append(operator_data)
            
            # Crear dataframe para visualizar
            metrics_df = pd.DataFrame(metrics_data)
            st.dataframe(metrics_df, width='stretch')
            
            # Si hay datos de propinas y tarifas, calcular la tasa de propinas
            if "tips" in uber_lyft.columns and "driver_pay" in uber_lyft.columns:
                st.subheader("💸 Análisis de Propinas")
                
                tip_analysis = uber_lyft.groupby("hvfhs_license_num").agg({
                    "tips": ["mean", "sum", lambda x: (x > 0).mean() * 100],
                    "driver_pay": "sum"
                }).reset_index()
                
                tip_analysis.columns = ["Empresa", "Propina Promedio", "Propinas Totales", "% Viajes con Propina", "Ingresos Totales"]
                tip_analysis["% sobre Ingresos"] = (tip_analysis["Propinas Totales"] / tip_analysis["Ingresos Totales"] * 100).round(2)
                
                # Formatear columnas
                tip_analysis["Propina Promedio"] = tip_analysis["Propina Promedio"].apply(lambda x: f"${x:.2f}")
                tip_analysis["Propinas Totales"] = tip_analysis["Propinas Totales"].apply(lambda x: f"${x:,.2f}")
                tip_analysis["% Viajes con Propina"] = tip_analysis["% Viajes con Propina"].apply(lambda x: f"{x:.1f}%")
                tip_analysis["% sobre Ingresos"] = tip_analysis["% sobre Ingresos"].apply(lambda x: f"{x:.2f}%")
                tip_analysis["Ingresos Totales"] = tip_analysis["Ingresos Totales"].apply(lambda x: f"${x:,.2f}")
                
                # Mostrar tabla de análisis de propinas
                st.dataframe(tip_analysis[["Empresa", "Propina Promedio", "% Viajes con Propina", "% sobre Ingresos"]], 
                            width='stretch')
                
                # Histograma de distribución de propinas
                uber_lyft_with_tips = uber_lyft[uber_lyft["tips"] > 0].copy()
                if len(uber_lyft_with_tips) > 0:
                    # Calcular porcentaje de propina
                    uber_lyft_with_tips["tip_percent"] = (uber_lyft_with_tips["tips"] / uber_lyft_with_tips["driver_pay"]) * 100
                    # Filtrar valores extremos para mejor visualización
                    uber_lyft_with_tips = uber_lyft_with_tips[uber_lyft_with_tips["tip_percent"] <= 30]
                    
                    fig_hist = px.histogram(
                        uber_lyft_with_tips, 
                        x="tip_percent",
                        color="hvfhs_license_num",
                        barmode="overlay",
                        opacity=0.7,
                        title="<b>Distribución del % de Propina (para viajes con propina)</b>",
                        labels={"tip_percent": "% de Propina", "hvfhs_license_num": "Empresa"},
                        color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"}
                    )
                    fig_hist.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
                    st.plotly_chart(fig_hist, width='stretch')
        
        # --- SEGUNDA COLUMNA: PATRONES DE VIAJE ---
        with col2:
            # Ingresos por empresa
            if "driver_pay" in uber_lyft.columns:
                income = uber_lyft.groupby("hvfhs_license_num")["driver_pay"].sum().reset_index()
                income.columns = ["Empresa", "Ingresos Totales"]
                income["Porcentaje"] = (income["Ingresos Totales"] / income["Ingresos Totales"].sum() * 100).round(1).astype(str) + '%'
                
                fig = px.pie(
                    income, 
                    values="Ingresos Totales", 
                    names="Empresa",
                    title="<b>Distribución de Ingresos por Empresa</b>",
                    color="Empresa",
                    color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
                    hover_data=["Porcentaje"]
                )
                fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.03, 0.03])
                fig.update_layout(
                    font_size=12,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig, width='stretch')
            
            # Comparativa por precio/milla y precio/minuto
            if all(col in uber_lyft.columns for col in ["driver_pay", "trip_miles", "trip_time"]):
                st.subheader("📊 Eficiencia por Distancia y Tiempo")
                
                # Calcular métricas de eficiencia
                efficiency = uber_lyft.groupby("hvfhs_license_num").apply(
                    lambda x: pd.Series({
                        "price_per_mile": x["driver_pay"].sum() / x["trip_miles"].sum(),
                        "price_per_minute": x["driver_pay"].sum() / (x["trip_time"].sum() / 60),
                        "miles_per_minute": (x["trip_miles"].sum() / (x["trip_time"].sum() / 60)),
                    })
                ).reset_index()
                
                # Crear dataframe para mostrar
                efficiency_formatted = efficiency.copy()
                efficiency_formatted["price_per_mile"] = efficiency_formatted["price_per_mile"].apply(lambda x: f"${x:.2f}/mi")
                efficiency_formatted["price_per_minute"] = efficiency_formatted["price_per_minute"].apply(lambda x: f"${x:.2f}/min")
                efficiency_formatted["miles_per_minute"] = efficiency_formatted["miles_per_minute"].apply(lambda x: f"{x:.2f} mi/min")
                
                # Cambiar nombres de columnas
                efficiency_formatted.columns = ["Empresa", "Precio por Milla", "Precio por Minuto", "Velocidad Promedio"]
                
                # Mostrar tabla de eficiencia
                st.dataframe(efficiency_formatted, width='stretch')
                
                # Gráfica comparativa de barras
                fig_bar = go.Figure()
                
                # Primera serie: Precio por milla
                fig_bar.add_trace(go.Bar(
                    x=efficiency["hvfhs_license_num"],
                    y=efficiency["price_per_mile"],
                    name="Precio por Milla ($)",
                    marker_color=["#276EF1", "#FF00BF"],
                    text=[f"${val:.2f}" for val in efficiency["price_per_mile"]],
                    textposition="auto"
                ))
                
                # Configurar layout
                fig_bar.update_layout(
                    title="<b>Comparativa de Precio por Milla</b>",
                    xaxis=dict(title="Empresa"),
                    yaxis=dict(title="Precio por Milla ($)"),
                    barmode="group",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig_bar, width='stretch')
    
    # Análisis por zona geográfica
    st.subheader("🌆 Concentración por Zonas")
    
    if "pickup_zone" in uber_lyft.columns:
        # Selección del número de zonas a mostrar
        top_n = st.slider("Número de zonas principales:", min_value=5, max_value=15, value=10, step=1)
        
        # Calculamos la concentración por zona
        zone_distribution = uber_lyft.groupby(["pickup_zone", "hvfhs_license_num"]).size().reset_index(name="viajes")
        
        # Obtenemos las top N zonas por volumen total
        top_zones = zone_distribution.groupby("pickup_zone")["viajes"].sum().nlargest(top_n).index
        zone_filtered = zone_distribution[zone_distribution["pickup_zone"].isin(top_zones)]
        
        # Crear gráfico comparativo de barras apiladas con zonas
        fig_zones = px.bar(
            zone_filtered,
            x="pickup_zone",
            y="viajes",
            color="hvfhs_license_num",
            title=f"<b>Top {top_n} Zonas de Recogida por Empresa</b>",
            labels={"pickup_zone": "Zona", "viajes": "Cantidad de Viajes", "hvfhs_license_num": "Empresa"},
            color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
            barmode="group"
        )
        
        fig_zones.update_layout(
            xaxis_tickangle=-45,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_zones, width='stretch')
        
        # Calcular dominancia por zona (qué empresa domina en cada zona)
        zone_dominance = zone_distribution.pivot(index="pickup_zone", columns="hvfhs_license_num", values="viajes").fillna(0)
        
        # Calcular porcentaje de dominancia
        zone_dominance["total"] = zone_dominance.sum(axis=1)
        for company in ["Uber", "Lyft"]:
            if company in zone_dominance.columns:
                zone_dominance[f"{company}_pct"] = (zone_dominance[company] / zone_dominance["total"] * 100).round(1)
        
        # Preparar datos para el mapa de calor
        dominance_df = zone_dominance.reset_index()
        dominance_top = dominance_df[dominance_df["pickup_zone"].isin(top_zones)]
        
        # Crear gráfico de calor de dominancia por zona
        fig_heatmap = go.Figure()
        
        if "Uber_pct" in dominance_top.columns and "Lyft_pct" in dominance_top.columns:
            fig_heatmap = px.imshow(
                dominance_top[["Uber_pct", "Lyft_pct"]].values,
                x=["Uber", "Lyft"],
                y=dominance_top["pickup_zone"],
                color_continuous_scale=[[0, "#FF00BF"], [0.5, "white"], [1, "#276EF1"]],
                labels=dict(x="Empresa", y="Zona", color="Porcentaje (%)"),
                title="<b>Porcentaje de Mercado por Zona</b>",
                text_auto=True,
                aspect="auto"
            )
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, width='stretch')
    else:
        st.warning("No hay datos de zonas disponibles para realizar este análisis.")
     
    # Análisis temporal (patrones por hora del día)
    st.subheader("⏰ Patrones por Hora del Día")
    
    # Conteo de viajes por hora
    hourly_trips = uber_lyft.groupby(["pickup_hour", "hvfhs_license_num"]).size().reset_index(name="viajes")
    
    # Gráfico de líneas comparativo
    fig_hourly = px.line(
        hourly_trips,
        x="pickup_hour",
        y="viajes",
        color="hvfhs_license_num",
        title="<b>Distribución de Viajes por Hora del Día</b>",
        labels={"pickup_hour": "Hora del Día", "viajes": "Cantidad de Viajes", "hvfhs_license_num": "Empresa"},
        color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
        markers=True
    )
    
    fig_hourly.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_hourly, width='stretch')
    
    # Análisis de cuotas de mercado por hora
    hourly_pivot = hourly_trips.pivot_table(index="pickup_hour", columns="hvfhs_license_num", values="viajes").fillna(0)
    hourly_pivot["total"] = hourly_pivot.sum(axis=1)
    for company in ["Uber", "Lyft"]:
        if company in hourly_pivot.columns:
            hourly_pivot[f"{company}_pct"] = (hourly_pivot[company] / hourly_pivot["total"] * 100).round(1)
    
    # Preparamos datos para gráfica
    hourly_shares = hourly_pivot.reset_index()
    
    # Gráfica de área para mostrar la evolución de cuota de mercado por hora
    fig_share = go.Figure()
    
    if "Uber_pct" in hourly_shares.columns:
        fig_share.add_trace(go.Scatter(
            x=hourly_shares["pickup_hour"],
            y=hourly_shares["Uber_pct"],
            mode="lines",
            stackgroup="one",
            name="Uber",
            line=dict(width=0),
            fillcolor="#276EF1"
        ))
    
    if "Lyft_pct" in hourly_shares.columns:
        fig_share.add_trace(go.Scatter(
            x=hourly_shares["pickup_hour"],
            y=hourly_shares["Lyft_pct"],
            mode="lines",
            stackgroup="one",
            name="Lyft",
            line=dict(width=0),
            fillcolor="#FF00BF"
        ))
    
    fig_share.update_layout(
        title="<b>Evolución de Cuota de Mercado por Hora</b>",
        xaxis=dict(title="Hora del Día", tickmode="linear", tick0=0, dtick=1),
        yaxis=dict(title="Porcentaje del Mercado (%)", range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_share, width='stretch')
    
    # Comparativa por día de la semana
    st.subheader("📅 Patrones por Día de la Semana")
    
    if "day_name" in uber_lyft.columns:
        day_col = "day_name"
        day_order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    else:
        day_col = "pickup_weekday"
        day_order = list(range(7))
    
    # Conteo de viajes por día de la semana
    daily_trips = uber_lyft.groupby([day_col, "hvfhs_license_num"]).size().reset_index(name="viajes")
    
    # Gráfico de barras comparativo
    fig_daily = px.bar(
        daily_trips,
        x=day_col,
        y="viajes",
        color="hvfhs_license_num",
        barmode="group",
        title="<b>Distribución de Viajes por Día de la Semana</b>",
        labels={day_col: "Día de la Semana", "viajes": "Cantidad de Viajes", "hvfhs_license_num": "Empresa"},
        color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
    )
    
    if day_col == "day_name":
        fig_daily.update_layout(xaxis={"categoryorder": "array", "categoryarray": day_order})
    
    fig_daily.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_daily, width='stretch')
    
    # Si hay datos de aeropuertos, analizar las diferencias en viajes desde/hacia aeropuertos
    if "to_airport" in uber_lyft.columns and "from_airport" in uber_lyft.columns:
        st.subheader("✈️ Análisis de Viajes a/desde Aeropuertos")
        
        # Filtros para aeropuertos
        airport_analysis = st.radio("Analizar viajes:", ["Hacia aeropuertos", "Desde aeropuertos"], horizontal=True)
        
        if airport_analysis == "Hacia aeropuertos":
            airport_col = "to_airport"
            direction_text = "hacia"
        else:
            airport_col = "from_airport"
            direction_text = "desde"
        
        # Conteo de viajes por aeropuerto
        airport_trips = uber_lyft.groupby([airport_col, "hvfhs_license_num"]).size().reset_index(name="viajes")
        
        # Asignamos etiqueta más descriptiva
        airport_trips[airport_col] = airport_trips[airport_col].map({1: f"Viajes {direction_text} aeropuertos", 0: "Otros viajes"})
        
        # Gráfico de barras comparativo
        fig_airport = px.bar(
            airport_trips,
            x=airport_col,
            y="viajes",
            color="hvfhs_license_num",
            barmode="group",
            title=f"<b>Comparativa de Viajes {direction_text.capitalize()} Aeropuertos</b>",
            labels={airport_col: "Tipo de Viaje", "viajes": "Cantidad de Viajes", "hvfhs_license_num": "Empresa"},
            color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"}
        )
        
        fig_airport.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_airport, width='stretch')
        
        # Calcular participación de mercado en viajes a/desde aeropuertos
        airport_share = uber_lyft[uber_lyft[airport_col] == 1].groupby("hvfhs_license_num").size().reset_index(name="viajes")
        if len(airport_share) > 0:
            airport_share["porcentaje"] = (airport_share["viajes"] / airport_share["viajes"].sum() * 100).round(1)
            
            # Gráfico de pie para participación en aeropuertos
            fig_airport_share = px.pie(
                airport_share,
                values="viajes",
                names="hvfhs_license_num",
                title=f"<b>Participación en Viajes {direction_text.capitalize()} Aeropuertos</b>",
                color="hvfhs_license_num",
                color_discrete_map={"Uber": "#276EF1", "Lyft": "#FF00BF"},
                hover_data=["porcentaje"]
            )
            
            fig_airport_share.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                pull=[0.03, 0.03]
            )
            
            st.plotly_chart(fig_airport_share, width='stretch')

with tab5:
    st.subheader("💰 Análisis de Ingresos e Impuestos")
    
    # Comprobar si existen las columnas necesarias
    income_cols = [
        "driver_pay", "tips", "base_passenger_fare", "tolls", "bcf", 
        "sales_tax", "congestion_surcharge", "airport_fee"
    ]
    
    available_cols = [col for col in income_cols if col in df_filtered.columns]
    
    if len(available_cols) == 0:
        st.warning("No hay columnas de ingresos o impuestos disponibles para analizar.")
    else:
        st.info(f"Columnas disponibles para análisis: {', '.join(available_cols)}")
        
        # Calcular totales
        totals = {}
        for col in available_cols:
            totals[col] = df_filtered[col].sum()
        
        # Mostrar totales en tarjetas
        st.subheader("Totales")
        cols = st.columns(min(4, len(available_cols)))
        
        for i, (name, value) in enumerate(totals.items()):
            display_name = {
                "driver_pay": "Pago al Conductor",
                "tips": "Propinas",
                "base_passenger_fare": "Tarifa Base",
                "tolls": "Peajes",
                "bcf": "Black Car Fund",
                "sales_tax": "Impuesto de Ventas",
                "congestion_surcharge": "Recargo por Congestión",
                "airport_fee": "Tarifa Aeroportuaria"
            }.get(name, name)
            
            cols[i % 4].metric(
                label=display_name,
                value=f"${value:,.2f}"
            )
        
        # Gráfico de composición de ingresos
        st.subheader("Composición de Ingresos y Cargos")
        income_composition = pd.DataFrame({
            "Concepto": [
                {
                    "driver_pay": "Pago al Conductor",
                    "tips": "Propinas",
                    "base_passenger_fare": "Tarifa Base",
                    "tolls": "Peajes",
                    "bcf": "Black Car Fund",
                    "sales_tax": "Impuesto de Ventas",
                    "congestion_surcharge": "Recargo por Congestión",
                    "airport_fee": "Tarifa Aeroportuaria"
                }.get(col, col) for col in available_cols
            ],
            "Monto": [totals[col] for col in available_cols]
        })
        
        # Gráfico de tarta
        fig1 = px.pie(
            income_composition,
            values="Monto",
            names="Concepto",
            title="Distribución de Ingresos y Cargos",
            hole=0.4
        )
        st.plotly_chart(fig1, width='stretch')
        
        # Análisis por empresa
        st.subheader("Análisis por Empresa")
        
        # Agrupar por empresa
        income_by_company = df_filtered.groupby("hvfhs_license_num")[available_cols].sum().reset_index()
        
        # Crear gráfico de barras apiladas para ver la composición por empresa
        fig2 = px.bar(
            income_by_company,
            x="hvfhs_license_num",
            y=available_cols,
            title="Composición de Ingresos por Empresa",
            labels={"hvfhs_license_num": "Empresa", "value": "Monto ($)", "variable": "Concepto"}
        )
        st.plotly_chart(fig2, width='stretch')
        
        # Análisis temporal si hay muchos días
        if df_filtered["pickup_datetime"].dt.date.nunique() > 3:
            st.subheader("Análisis Temporal de Ingresos")
            
            # Agrupar por fecha
            df_filtered["pickup_date"] = df_filtered["pickup_datetime"].dt.date
            daily_income = df_filtered.groupby(["pickup_date", "hvfhs_license_num"])["driver_pay"].sum().reset_index()
            
            # Gráfico de tendencia
            fig3 = px.line(
                daily_income,
                x="pickup_date",
                y="driver_pay",
                color="hvfhs_license_num",
                markers=True,
                title="Evolución de Ingresos Diarios",
                labels={"pickup_date": "Fecha", "driver_pay": "Ingresos ($)", "hvfhs_license_num": "Empresa"}
            )
            st.plotly_chart(fig3, width='stretch')
        
        # Análisis de relación entre variables
        if {"driver_pay", "tips"}.issubset(available_cols):
            st.subheader("Relación entre Ingresos y Propinas")
            
            # Calcular porcentaje de propina
            df_filtered["tip_percent"] = (df_filtered["tips"] / df_filtered["driver_pay"]) * 100
            
            # Filtrar datos válidos
            valid_tips = df_filtered[(df_filtered["tip_percent"] <= 100) & (df_filtered["tip_percent"] >= 0)]
            
            # Scatter plot
            fig4 = px.scatter(
                valid_tips,
                x="driver_pay",
                y="tips",
                color="hvfhs_license_num",
                opacity=0.6,
                trendline="ols",
                title="Relación entre Tarifa y Propina",
                labels={"driver_pay": "Tarifa ($)", "tips": "Propina ($)", "hvfhs_license_num": "Empresa"}
            )
            st.plotly_chart(fig4, width='stretch')
            
            # Distribución del porcentaje de propina
            fig5 = px.histogram(
                valid_tips,
                x="tip_percent",
                color="hvfhs_license_num",
                nbins=50,
                opacity=0.7,
                barmode="overlay",
                title="Distribución del Porcentaje de Propina",
                labels={"tip_percent": "Porcentaje de Propina (%)", "hvfhs_license_num": "Empresa"}
            )
            fig5.update_layout(bargap=0.1)
            st.plotly_chart(fig5, width='stretch')

with tab6:
    st.subheader("✈️ Análisis de Viajes a Aeropuertos")
    
    # Verificar si existen las columnas necesarias
    if "to_airport" not in df_filtered.columns or "from_airport" not in df_filtered.columns:
        st.warning("""
        ⚠️ Los datos no contienen información sobre viajes a aeropuertos.
        
        Esta funcionalidad requiere las columnas 'to_airport' y 'from_airport' en el dataset.
        """)
    else:
        # Banner informativo
        st.info("""
        📍 **Análisis de Conectividad Aeroportuaria**: Este módulo analiza los patrones de viajes hacia y desde 
        los principales aeropuertos de NYC (JFK, LaGuardia, Newark). Incluye métricas de volumen, tarifas, 
        distribución temporal y análisis comparativo.
        """)
        
        # Filtrar datos de aeropuertos
        to_airport_trips = df_filtered[df_filtered["to_airport"] == True]
        from_airport_trips = df_filtered[df_filtered["from_airport"] == True]
        all_airport_trips = df_filtered[(df_filtered["to_airport"] == True) | (df_filtered["from_airport"] == True)]
        
        # Contadores
        to_airport_count = len(to_airport_trips)
        from_airport_count = len(from_airport_trips)
        all_airport_count = len(all_airport_trips)
        total_trips = len(df_filtered)
        
        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric(
            "Viajes Hacia Aeropuertos", 
            f"{to_airport_count:,}",
            f"{to_airport_count/total_trips*100:.1f}% del total"
        )
        
        col2.metric(
            "Viajes Desde Aeropuertos", 
            f"{from_airport_count:,}",
            f"{from_airport_count/total_trips*100:.1f}% del total"
        )
        
        col3.metric(
            "Total Viajes Aeroportuarios", 
            f"{all_airport_count:,}",
            f"{all_airport_count/total_trips*100:.1f}% del total"
        )
        
        if "driver_pay" in df_filtered.columns and all_airport_count > 0:
            avg_airport_fare = all_airport_trips["driver_pay"].mean()
            col4.metric(
                "Tarifa Promedio Aeropuertos", 
                f"${avg_airport_fare:.2f}"
            )
        
        # Crear sub-pestañas para análisis detallado
        airport_tabs = st.tabs(["Viajes Hacia Aeropuertos", "Viajes Desde Aeropuertos", "Ambas Direcciones"])
        
        # TAB 1: VIAJES HACIA AEROPUERTOS
        with airport_tabs[0]:
            if to_airport_count == 0:
                st.warning("No hay viajes hacia aeropuertos en los datos filtrados.")
            else:
                st.subheader("🛫 Características de Viajes Hacia Aeropuertos")
                
                # Métricas principales en tarjetas
                col1, col2, col3 = st.columns(3)
                
                col1.metric(
                    "Total Viajes hacia Aeropuertos", 
                    f"{to_airport_count:,}", 
                    f"{to_airport_count/total_trips*100:.1f}% del total"
                )
                
                # Distancia promedio
                if "trip_miles" in df_filtered.columns:
                    avg_miles_airport = to_airport_trips["trip_miles"].mean()
                    avg_miles_all = df_filtered["trip_miles"].mean()
                    miles_diff = avg_miles_airport - avg_miles_all
                    
                    col2.metric(
                        "Distancia Promedio", 
                        f"{avg_miles_airport:.2f} millas", 
                        f"{miles_diff:+.2f} vs promedio general",
                        delta_color="normal"
                    )
                
                # Tarifa promedio
                if "driver_pay" in df_filtered.columns:
                    avg_fare_airport = to_airport_trips["driver_pay"].mean()
                    avg_fare_all = df_filtered["driver_pay"].mean()
                    fare_diff = avg_fare_airport - avg_fare_all
                    
                    col3.metric(
                        "Tarifa Promedio", 
                        f"${avg_fare_airport:.2f}", 
                        f"${fare_diff:+.2f} vs promedio general",
                        delta_color="normal"
                    )
                
                # Análisis por empresa
                st.subheader("Distribución por Empresa")
                
                company_airport = to_airport_trips.groupby("hvfhs_license_num").size().reset_index(name="viajes")
                company_airport["porcentaje"] = (company_airport["viajes"] / company_airport["viajes"].sum() * 100).round(1)
                
                # Gráfico de pastel
                fig1 = px.pie(
                    company_airport,
                    names="hvfhs_license_num",
                    values="viajes",
                    title="Participación de Empresas en Viajes hacia Aeropuertos",
                    hole=0.4,
                    hover_data=["porcentaje"]
                )
                
                fig1.update_traces(textinfo="percent+label")
                st.plotly_chart(fig1, width='stretch')
                
                # Distribución por hora del día
                st.subheader("Distribución por Hora del Día")
                
                hourly_to_airport = to_airport_trips.groupby("pickup_hour").size().reset_index(name="viajes")
                hourly_general = df_filtered.groupby("pickup_hour").size().reset_index(name="total_viajes")
                
                hourly_combined = hourly_to_airport.merge(hourly_general, on="pickup_hour", how="right")
                hourly_combined["viajes"] = hourly_combined["viajes"].fillna(0)
                hourly_combined["porcentaje"] = (hourly_combined["viajes"] / hourly_combined["total_viajes"] * 100).round(1)
                
                # Crear figura con dos ejes Y
                fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig2.add_trace(
                    go.Bar(
                        x=hourly_combined["pickup_hour"],
                        y=hourly_combined["viajes"],
                        name="Viajes hacia Aeropuertos",
                        marker_color="#FF9800"
                    ),
                    secondary_y=False
                )
                
                fig2.add_trace(
                    go.Scatter(
                        x=hourly_combined["pickup_hour"],
                        y=hourly_combined["porcentaje"],
                        name="% del Total",
                        mode="lines+markers",
                        marker_color="#2196F3",
                        line=dict(width=3)
                    ),
                    secondary_y=True
                )
                
                fig2.update_layout(
                    title="Viajes hacia Aeropuertos por Hora del Día",
                    xaxis_title="Hora del Día",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                )
                
                fig2.update_yaxes(title_text="Número de Viajes", secondary_y=False)
                fig2.update_yaxes(title_text="% del Total de Viajes", secondary_y=True)
                
                st.plotly_chart(fig2, width='stretch')
                
                # Si hay datos de aeropuertos específicos
                if "DOLocationID" in df_filtered.columns and AIRPORT_ZONES:
                    st.subheader("Distribución por Aeropuerto")
                    
                    airport_distribution = []
                    for airport_id in AIRPORT_ZONES:
                        if airport_id in AIRPORT_NAMES:
                            airport_trips = to_airport_trips[to_airport_trips["DOLocationID"] == airport_id]
                            airport_distribution.append({
                                "Aeropuerto": AIRPORT_NAMES[airport_id],
                                "Viajes": len(airport_trips),
                                "Porcentaje": len(airport_trips) / to_airport_count * 100
                            })
                    
                    if airport_distribution:
                        airport_df = pd.DataFrame(airport_distribution)
                        
                        fig3 = px.pie(
                            airport_df,
                            names="Aeropuerto",
                            values="Viajes",
                            title="Distribución de Viajes por Aeropuerto",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        
                        fig3.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig3, width='stretch')
        
        # TAB 2: VIAJES DESDE AEROPUERTOS
        with airport_tabs[1]:
            if from_airport_count == 0:
                st.warning("No hay viajes desde aeropuertos en los datos filtrados.")
            else:
                st.subheader("🛬 Características de Viajes Desde Aeropuertos")
                
                # Métricas principales en tarjetas
                col1, col2, col3 = st.columns(3)
                
                col1.metric(
                    "Total Viajes desde Aeropuertos", 
                    f"{from_airport_count:,}", 
                    f"{from_airport_count/total_trips*100:.1f}% del total"
                )
                
                # Distancia promedio
                if "trip_miles" in df_filtered.columns:
                    avg_miles_airport = from_airport_trips["trip_miles"].mean()
                    avg_miles_all = df_filtered["trip_miles"].mean()
                    miles_diff = avg_miles_airport - avg_miles_all
                    
                    col2.metric(
                        "Distancia Promedio", 
                        f"{avg_miles_airport:.2f} millas", 
                        f"{miles_diff:+.2f} vs promedio general",
                        delta_color="normal"
                    )
                
                # Tarifa promedio
                if "driver_pay" in df_filtered.columns:
                    avg_fare_airport = from_airport_trips["driver_pay"].mean()
                    avg_fare_all = df_filtered["driver_pay"].mean()
                    fare_diff = avg_fare_airport - avg_fare_all
                    
                    col3.metric(
                        "Tarifa Promedio", 
                        f"${avg_fare_airport:.2f}", 
                        f"${fare_diff:+.2f} vs promedio general",
                        delta_color="normal"
                    )
                
                # Análisis por empresa
                st.subheader("Distribución por Empresa")
                
                company_airport = from_airport_trips.groupby("hvfhs_license_num").size().reset_index(name="viajes")
                company_airport["porcentaje"] = (company_airport["viajes"] / company_airport["viajes"].sum() * 100).round(1)
                
                # Gráfico de pastel
                fig1 = px.pie(
                    company_airport,
                    names="hvfhs_license_num",
                    values="viajes",
                    title="Participación de Empresas en Viajes desde Aeropuertos",
                    hole=0.4,
                    hover_data=["porcentaje"]
                )
                
                fig1.update_traces(textinfo="percent+label")
                st.plotly_chart(fig1, width='stretch')
                
                # Distribución por hora del día
                st.subheader("Distribución por Hora del Día")
                
                hourly_from_airport = from_airport_trips.groupby("pickup_hour").size().reset_index(name="viajes")
                hourly_general = df_filtered.groupby("pickup_hour").size().reset_index(name="total_viajes")
                
                hourly_combined = hourly_from_airport.merge(hourly_general, on="pickup_hour", how="right")
                hourly_combined["viajes"] = hourly_combined["viajes"].fillna(0)
                hourly_combined["porcentaje"] = (hourly_combined["viajes"] / hourly_combined["total_viajes"] * 100).round(1)
                
                # Crear figura con dos ejes Y
                fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig2.add_trace(
                    go.Bar(
                        x=hourly_combined["pickup_hour"],
                        y=hourly_combined["viajes"],
                        name="Viajes desde Aeropuertos",
                        marker_color="#4CAF50"
                    ),
                    secondary_y=False
                )
                
                fig2.add_trace(
                    go.Scatter(
                        x=hourly_combined["pickup_hour"],
                        y=hourly_combined["porcentaje"],
                        name="% del Total",
                        mode="lines+markers",
                        marker_color="#2196F3",
                        line=dict(width=3)
                    ),
                    secondary_y=True
                )
                
                fig2.update_layout(
                    title="Viajes desde Aeropuertos por Hora del Día",
                    xaxis_title="Hora del Día",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                )
                
                fig2.update_yaxes(title_text="Número de Viajes", secondary_y=False)
                fig2.update_yaxes(title_text="% del Total de Viajes", secondary_y=True)
                
                st.plotly_chart(fig2, width='stretch')
                
                # Si hay datos de aeropuertos específicos
                if "PULocationID" in df_filtered.columns and AIRPORT_ZONES:
                    st.subheader("Distribución por Aeropuerto")
                    
                    airport_distribution = []
                    for airport_id in AIRPORT_ZONES:
                        if airport_id in AIRPORT_NAMES:
                            airport_trips = from_airport_trips[from_airport_trips["PULocationID"] == airport_id]
                            airport_distribution.append({
                                "Aeropuerto": AIRPORT_NAMES[airport_id],
                                "Viajes": len(airport_trips),
                                "Porcentaje": len(airport_trips) / from_airport_count * 100
                            })
                    
                    if airport_distribution:
                        airport_df = pd.DataFrame(airport_distribution)
                        
                        fig3 = px.pie(
                            airport_df,
                            names="Aeropuerto",
                            values="Viajes",
                            title="Distribución de Viajes por Aeropuerto",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        
                        fig3.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig3, width='stretch')
        
        # TAB 3: ANÁLISIS COMBINADO
        with airport_tabs[2]:
            st.subheader("🔄 Análisis Combinado de Viajes Aeroportuarios")
            
            if all_airport_count == 0:
                st.warning("No hay viajes aeroportuarios en los datos filtrados.")
            else:
                # Comparación de volúmenes
                st.subheader("Comparación de Volúmenes")
                
                volume_data = pd.DataFrame({
                    "Tipo": ["Hacia Aeropuertos", "Desde Aeropuertos"],
                    "Viajes": [to_airport_count, from_airport_count],
                    "Porcentaje": [to_airport_count/total_trips*100, from_airport_count/total_trips*100]
                })
                
                fig1 = px.bar(
                    volume_data,
                    x="Tipo",
                    y="Viajes",
                    title="Comparación de Volúmenes de Viajes Aeroportuarios",
                    text="Viajes",
                    color="Tipo",
                    color_discrete_sequence=["#FF9800", "#4CAF50"]
                )
                
                fig1.update_traces(texttemplate='%{text:,}', textposition='outside')
                st.plotly_chart(fig1, width='stretch')
                
                # Comparación de tarifas
                if "driver_pay" in df_filtered.columns:
                    st.subheader("Comparación de Tarifas")
                    
                    # Crear DataFrame para comparación
                    fare_comparison = pd.DataFrame({
                        "Tipo": ["Hacia Aeropuertos"] * len(to_airport_trips) + ["Desde Aeropuertos"] * len(from_airport_trips),
                        "Tarifa": list(to_airport_trips["driver_pay"]) + list(from_airport_trips["driver_pay"])
                    })
                    
                    # Mostrar estadísticas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.dataframe(
                            fare_comparison.groupby("Tipo")["Tarifa"].describe().round(2),
                            use_container_width=True
                        )
                    
                    with col2:
                        fig2 = px.box(
                            fare_comparison,
                            x="Tipo",
                            y="Tarifa",
                            title="Distribución de Tarifas por Tipo de Viaje",
                            color="Tipo",
                            color_discrete_sequence=["#FF9800", "#4CAF50"]
                        )
                        
                        st.plotly_chart(fig2, width='stretch')
                
                # Análisis temporal
                if "day_name" in df_filtered.columns:
                    st.subheader("Análisis Temporal por Día de la Semana")
                    
                    # Crear datos temporales
                    to_airport_daily = to_airport_trips.groupby("day_name").size().reset_index(name="hacia_aeropuertos")
                    from_airport_daily = from_airport_trips.groupby("day_name").size().reset_index(name="desde_aeropuertos")
                    
                    daily_combined = to_airport_daily.merge(from_airport_daily, on="day_name", how="outer").fillna(0)
                    
                    # Ordenar días de la semana
                    day_order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                    daily_combined["day_name"] = pd.Categorical(daily_combined["day_name"], categories=day_order, ordered=True)
                    daily_combined = daily_combined.sort_values("day_name")
                    
                    fig3 = go.Figure()
                    
                    fig3.add_trace(go.Scatter(
                        x=daily_combined["day_name"],
                        y=daily_combined["hacia_aeropuertos"],
                        mode='lines+markers',
                        name='Hacia Aeropuertos',
                        line=dict(color='#FF9800', width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig3.add_trace(go.Scatter(
                        x=daily_combined["day_name"],
                        y=daily_combined["desde_aeropuertos"],
                        mode='lines+markers',
                        name='Desde Aeropuertos',
                        line=dict(color='#4CAF50', width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig3.update_layout(
                        title="Tendencia de Viajes Aeroportuarios por Día de la Semana",
                        xaxis_title="Día de la Semana",
                        yaxis_title="Número de Viajes",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    
                    st.plotly_chart(fig3, width='stretch')

with tab7:
    st.subheader("🤖 Modelos Predictivos y de Clasificación")
    
    # Banner informativo
    st.info("""
    🧠 **Machine Learning para Análisis de Viajes**
    
    Esta sección utiliza modelos de machine learning entrenados para:
    - **Predicción de Tarifas**: Estima el costo de un viaje basado en sus características
    - **Clasificación de Aeropuertos**: Determina si un viaje tiene destino a un aeropuerto
    - **Análisis de Features**: Muestra qué variables son más importantes para las predicciones
    """)
    
    # Verificar si los modelos están disponibles
    try:
        import model_utils
        available_models = model_utils.get_available_models()
        
        if available_models:
            # Mostrar modelos disponibles
            st.success(f"✅ {len(available_models)} modelo(s) cargado(s) exitosamente")
            
            # Información de modelos en expander
            with st.expander("Ver detalles de modelos disponibles"):
                for model_name, model_info in available_models.items():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{model_name.replace('_', ' ').title()}**")
                    with col2:
                        model_type = "Red Neuronal" if model_info['type'] == 'neural_network' else "Modelo Tradicional"
                        st.write(f"Tipo: {model_type}")
                    with col3:
                        if 'performance' in model_info:
                            st.write(f"Performance: {model_info['performance']:.3f}")
            
            # Crear tabs para diferentes funcionalidades
            pred_tabs = st.tabs(["Predicción de Tarifa", "Clasificación de Aeropuertos", "Análisis de Features"])
            
            # Tab 1: Predicción de Tarifa
            with pred_tabs[0]:
                st.subheader("Predictor de Tarifas")
                
                # Explicación
                st.info("""
                Ingresa las características del viaje para obtener una estimación de la tarifa.
                El modelo considera factores como distancia, duración, hora del día, y empresa.
                """)
                
                # Formulario para ingresar datos
                with st.form("fare_prediction_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        trip_distance = st.number_input("Distancia del viaje (millas)", min_value=0.1, max_value=50.0, value=5.0, step=0.1)
                        trip_duration = st.number_input("Duración del viaje (minutos)", min_value=1, max_value=120, value=15, step=1)
                        pickup_hour = st.slider("Hora de recogida", min_value=0, max_value=23, value=12)
                        
                    with col2:
                        company = st.selectbox("Empresa", options=["Uber", "Lyft", "Via", "Juno"], index=0)
                        pickup_weekday = st.selectbox("Día de la semana", 
                                                    options=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
                                                    index=0)
                        
                        # Convertir día a número
                        weekday_map = {"Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, 
                                     "Viernes": 4, "Sábado": 5, "Domingo": 6}
                        weekday_num = weekday_map[pickup_weekday]
                    
                    # Selector de modelo
                    fare_models = [name for name, info in available_models.items() if 'fare' in name.lower()]
                    if fare_models:
                        selected_model = st.selectbox("Modelo a usar", options=fare_models, 
                                                    format_func=lambda x: x.replace('_', ' ').title())
                    
                    submitted = st.form_submit_button("Predecir Tarifa")
                
                if submitted and fare_models:
                    # Crear DataFrame con las características
                    predict_df = pd.DataFrame({
                        'trip_miles': [trip_distance],
                        'trip_time': [trip_duration * 60],  # convertir a segundos
                        'pickup_hour': [pickup_hour],
                        'pickup_weekday': [weekday_num],
                        'hvfhs_license_num': [company],
                    })
                    
                    # Realizar predicción
                    try:
                        predicted_fare = model_utils.predict_fare(predict_df, selected_model)
                        
                        if predicted_fare is not None:
                            # Mostrar predicción
                            st.success(f"💵 El costo estimado del viaje es: **${predicted_fare:.2f}**")
                            
                            # Mostrar información del modelo usado
                            model_info = available_models[selected_model]
                            model_type = "Red Neuronal" if model_info['type'] == 'neural_network' else "Modelo Tradicional"
                            st.info(f"Predicción realizada con: {selected_model.replace('_', ' ').title()} ({model_type})")
                            
                            # Visualizar con un medidor
                            if predicted_fare <= 100:
                                fig = go.Figure(go.Indicator(
                                    mode = "gauge+number",
                                    value = predicted_fare,
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title = {'text': "Tarifa Estimada ($)"},
                                    gauge = {
                                        'axis': {'range': [None, 100]},
                                        'steps': [
                                            {'range': [0, 25], 'color': "lightgreen"},
                                            {'range': [25, 50], 'color': "yellow"},
                                            {'range': [50, 75], 'color': "orange"},
                                            {'range': [75, 100], 'color': "red"}
                                        ],
                                        'threshold': {
                                            'line': {'color': "darkred", 'width': 4},
                                            'thickness': 0.75,
                                            'value': predicted_fare
                                        }
                                    }
                                ))
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning(f"La tarifa estimada (${predicted_fare:.2f}) es muy alta. Verifica los datos ingresados.")
                        else:
                            st.error("No se pudo generar una predicción con los datos proporcionados.")
                    except Exception as e:
                        st.error(f"Error al predecir: {str(e)}")
                        st.write("Detalles del error para depuración:")
                        st.code(str(e))
                elif submitted:
                    st.error("No hay modelos de predicción de tarifas disponibles.")
        
        # Tab 2: Clasificación de Aeropuertos
        with pred_tabs[1]:
            st.subheader("Clasificador de Viajes a Aeropuertos")
            
            # Explicación
            st.info("""
            Este modelo clasifica si un viaje tiene como destino un aeropuerto en función de sus características.
            Ingresa los detalles del viaje para obtener una clasificación y la probabilidad asociada.
            """)
            
            # Formulario para ingresar características
            with st.form("airport_classification_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    trip_distance = st.number_input("Distancia del viaje (millas)", min_value=0.1, max_value=50.0, value=10.0, step=0.5, key="airport_dist")
                    pickup_hour = st.slider("Hora de recogida", min_value=0, max_value=23, value=8, key="airport_hour")
                    
                with col2:
                    trip_duration = st.number_input("Duración del viaje (minutos)", min_value=1, max_value=120, value=25, step=1, key="airport_duration")
                    company = st.selectbox("Empresa", options=["Uber", "Lyft", "Via", "Juno"], index=0, key="airport_company")
                
                submitted = st.form_submit_button("Clasificar Viaje")
            
            if submitted:
                # Crear un DataFrame con las características ingresadas
                predict_df = pd.DataFrame({
                    'trip_miles': [trip_distance],
                    'trip_time': [trip_duration * 60],  # convertir a segundos
                    'pickup_hour': [pickup_hour],
                    'hvfhs_license_num': [company],
                })
                
                # Agregar características adicionales que podrían requerir los modelos
                predict_df['pickup_weekday'] = 1  # podríamos ajustar esto
                
                # Intentar predecir
                try:
                    predictions, probabilities = model_utils.predict_airport(predict_df)
                    
                    if predictions is not None:
                        # Mostrar predicción
                        result = "Viaje a Aeropuerto" if predictions[0] == 1 else "Viaje Normal (No a Aeropuerto)"
                        
                        # Color según la predicción
                        result_color = "green" if predictions[0] == 1 else "blue"
                        
                        st.markdown(f"<h3 style='color:{result_color};'>Resultado: {result}</h3>", unsafe_allow_html=True)
                        
                        # Mostrar probabilidad
                        if probabilities is not None:
                            prob_value = probabilities[0] if predictions[0] == 1 else 1 - probabilities[0]
                            st.metric(
                                label="Confianza de la predicción",
                                value=f"{prob_value*100:.1f}%"
                            )
                            
                            # Visualizar probabilidad
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = prob_value*100,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Confianza (%)"},
                                gauge = {
                                    'axis': {'range': [None, 100]},
                                    'steps': [
                                        {'range': [0, 30], 'color': "lightgray"},
                                        {'range': [30, 70], 'color': "gray"},
                                        {'range': [70, 100], 'color': result_color}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': prob_value*100
                                    }
                                }
                            ))
                            st.plotly_chart(fig)
                    else:
                        st.error("No se pudo generar una clasificación con los datos proporcionados.")
                except Exception as e:
                    st.error(f"Error al clasificar: {e}")
        
        # Tab 3: Análisis de Features
        with pred_tabs[2]:
            st.subheader("Importancia de Variables")
            
            # Seleccionar modelo para analizar
            model_for_analysis = st.selectbox(
                "Seleccionar modelo para analizar",
                options=[name for name, info in available_models.items() if 'nn' not in name],
                format_func=lambda x: available_models[x]['type'] if x in available_models else x
            )
            
            if model_for_analysis:
                # Obtener importancia de features
                try:
                    importances = model_utils.get_feature_importance(model_for_analysis)
                    
                    if importances:
                        # Convertir a DataFrame para visualización
                        imp_df = pd.DataFrame(
                            {'Feature': list(importances.keys()), 'Importance': list(importances.values())}
                        ).sort_values('Importance', ascending=False).head(15)
                        
                        # Gráfico de barras horizontales
                        fig = px.bar(
                            imp_df,
                            x='Importance',
                            y='Feature',
                            orientation='h',
                            title=f"Top 15 Variables más Importantes para {available_models[model_for_analysis]['type']}",
                            labels={'Importance': 'Importancia Relativa', 'Feature': 'Variable'},
                            color='Importance',
                            color_continuous_scale='Viridis'
                        )
                        
                        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                        st.plotly_chart(fig, width='stretch')
                        
                        # Mostrar tabla con importancias
                        with st.expander("Ver tabla de importancias"):
                            st.table(imp_df)
                    else:
                        st.warning("No se pudieron obtener las importancias de las variables para este modelo.")
                except Exception as e:
                    st.error(f"Error al analizar la importancia de variables: {e}")
    else:
        st.warning("⚠️ No se encontraron modelos de machine learning.")
        st.info("""
        Para usar la funcionalidad de modelos de machine learning:
        1. Asegúrate de tener instaladas las dependencias necesarias (scikit-learn, tensorflow, joblib)
        2. Ejecuta el script train_models.py para entrenar los modelos
        3. Verifica que la carpeta 'models/' existe y contiene los archivos de modelos
        """)
except Exception as e:
    st.error(f"Error al cargar los módulos de machine learning: {e}")
    st.info("""
    Para usar la funcionalidad de modelos de machine learning:
    1. Asegúrate de tener instaladas las dependencias necesarias (scikit-learn, tensorflow, joblib)
    2. Ejecuta el script train_models.py para entrenar los modelos
    3. Verifica que la carpeta 'models/' existe y contiene los archivos de modelos
    """)

# Nueva pestaña de Modelos de ML
with tab8:
    st.subheader("🤖 Modelos Predictivos y de Clasificación")
    
    # Importar model_utils
    try:
        import model_utils
        
        # Banner informativo
        st.info("""
        Esta sección permite realizar predicciones utilizando modelos de machine learning entrenados con datos históricos de viajes.
        Los modelos incluyen algoritmos tradicionales (RandomForest, XGBoost) y redes neuronales entrenadas con TensorFlow.
        """)
        
        # Verificar si hay modelos disponibles
        available_models = model_utils.get_available_models()
        
        if not available_models:
            st.warning("""
            ⚠️ No hay modelos entrenados disponibles. 
            
            Para empezar a usar esta funcionalidad:
            1. Ejecuta el script `train_models.py` para entrenar los modelos utilizando tu GPU
            2. Los modelos se guardarán automáticamente en la carpeta "models/"
            3. Recarga esta página para utilizar los modelos entrenados
            """)
            
            # Mostrar código de ejemplo
            with st.expander("Cómo entrenar los modelos"):
                st.code("""
                # En una terminal, navega a la carpeta del proyecto y ejecuta:
                cd c:\\Users\\diego\\Workspace\\Escuela\\mineria
                python train_models.py
                
                # Este proceso aprovechará tu GPU para entrenar varios modelos:
                # 1. Predicción de costo de viaje
                # 2. Clasificación de viajes a aeropuertos
                # 3. Predicción de duración de viaje
                """)
        else:
            # Mostrar información de modelos disponibles
            st.subheader("Modelos Disponibles")
            
            # Crear tarjetas para mostrar cada modelo
            num_models = len(available_models)
            cols = st.columns(num_models if num_models <= 3 else 3)
            
            for i, (model_name, model_info) in enumerate(available_models.items()):
                col_idx = i % 3
                with cols[col_idx]:
                    # Determinar el tipo de modelo para mostrar
                    model_type = "Red Neuronal" if model_info['type'] == 'neural_network' else "Modelo Tradicional"
                    
                    # Obtener métricas para mostrar
                    metrics = model_info.get('metrics', {})
                    if 'rmse' in metrics:
                        performance = f"RMSE: {metrics['rmse']:.2f}"
                    elif 'accuracy' in metrics:
                        performance = f"Precisión: {metrics['accuracy']:.2%}"
                    else:
                        performance = "Sin métricas"
                    
                    st.metric(
                        label=model_name.replace('_', ' ').title(),
                        value=model_type,
                        delta=performance
                    )
            
            # Crear tabs para diferentes funcionalidades
            pred_tabs = st.tabs(["Predicción de Tarifa", "Clasificación de Aeropuertos", "Análisis de Features"])
            
            # Tab 1: Predicción de Tarifa
            with pred_tabs[0]:
                st.subheader("Predicción de Costo de Viaje")
                
                # Formulario para ingresar características
                with st.form("fare_prediction_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        trip_distance = st.number_input("Distancia del viaje (millas)", min_value=0.1, max_value=50.0, value=5.0, step=0.5)
                        trip_duration = st.number_input("Duración del viaje (minutos)", min_value=1, max_value=120, value=15, step=1)
                        
                    with col2:
                        pickup_hour = st.slider("Hora de recogida", min_value=0, max_value=23, value=12)
                        company = st.selectbox("Empresa", options=["Uber", "Lyft", "Via", "Juno"], index=0)
                    
                    to_airport = st.checkbox("¿Viaje hacia el aeropuerto?")
                    from_airport = st.checkbox("¿Viaje desde el aeropuerto?")
                    
                    submitted = st.form_submit_button("Predecir Tarifa")
                
                if submitted:
                    # Crear un DataFrame con las características ingresadas
                    predict_df = pd.DataFrame({
                        'trip_miles': [trip_distance],
                        'trip_time': [trip_duration * 60],  # convertir a segundos
                        'pickup_hour': [pickup_hour]
                    })
                    
                    # Intentar predecir con diferentes modelos disponibles
                    try:
                        # Obtener modelos de predicción de tarifas disponibles
                        fare_models = [name for name in available_models.keys() if 'driver_pay' in name]
                        
                        if fare_models:
                            # Usar el primer modelo disponible
                            selected_model = fare_models[0]
                            prediction = model_utils.predict_fare(predict_df, model_name=selected_model)
                            
                            if prediction is not None and len(prediction) > 0:
                                predicted_fare = prediction[0]
                                
                                # Mostrar predicción
                                st.success(f"💵 El costo estimado del viaje es: **${predicted_fare:.2f}**")
                                
                                # Mostrar información del modelo usado
                                model_info = available_models[selected_model]
                                model_type = "Red Neuronal" if model_info['type'] == 'neural_network' else "Modelo Tradicional"
                                st.info(f"Predicción realizada con: {selected_model.replace('_', ' ').title()} ({model_type})")
                                
                                # Visualizar con un medidor
                                if predicted_fare <= 100:
                                    fig = go.Figure(go.Indicator(
                                        mode = "gauge+number",
                                        value = predicted_fare,
                                        domain = {'x': [0, 1], 'y': [0, 1]},
                                        title = {'text': "Tarifa Estimada ($)"},
                                        gauge = {
                                            'axis': {'range': [None, 100]},
                                            'steps': [
                                                {'range': [0, 25], 'color': "lightgreen"},
                                                {'range': [25, 50], 'color': "yellow"},
                                                {'range': [50, 75], 'color': "orange"},
                                                {'range': [75, 100], 'color': "red"}
                                            ],
                                            'threshold': {
                                                'line': {'color': "darkred", 'width': 4},
                                                'thickness': 0.75,
                                                'value': predicted_fare
                                            }
                                        }
                                    ))
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.warning(f"La tarifa estimada (${predicted_fare:.2f}) es muy alta. Verifica los datos ingresados.")
                            else:
                                st.error("No se pudo generar una predicción con los datos proporcionados.")
                        else:
                            st.error("No hay modelos de predicción de tarifas disponibles.")
                    except Exception as e:
                        st.error(f"Error al predecir: {str(e)}")
                        st.write("Detalles del error para depuración:")
                        st.code(str(e))
            
            # Tab 2: Clasificación de Aeropuertos
            with pred_tabs[1]:
                st.subheader("Clasificador de Viajes a Aeropuertos")
                
                # Explicación
                st.info("""
                Este modelo clasifica si un viaje tiene como destino un aeropuerto en función de sus características.
                Ingresa los detalles del viaje para obtener una clasificación y la probabilidad asociada.
                """)
                
                # Formulario para ingresar características
                with st.form("airport_classification_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        trip_distance = st.number_input("Distancia del viaje (millas)", min_value=0.1, max_value=50.0, value=10.0, step=0.5, key="airport_dist")
                        pickup_hour = st.slider("Hora de recogida", min_value=0, max_value=23, value=8, key="airport_hour")
                        
                    with col2:
                        trip_duration = st.number_input("Duración del viaje (minutos)", min_value=1, max_value=120, value=25, step=1, key="airport_duration")
                        company = st.selectbox("Empresa", options=["Uber", "Lyft", "Via", "Juno"], index=0, key="airport_company")
                    
                    submitted = st.form_submit_button("Clasificar Viaje")
                
                if submitted:
                    # Crear un DataFrame con las características ingresadas
                    predict_df = pd.DataFrame({
                        'trip_miles': [trip_distance],
                        'trip_time': [trip_duration * 60],  # convertir a segundos
                        'pickup_hour': [pickup_hour],
                        'hvfhs_license_num': [company],
                    })
                    
                    # Agregar características adicionales que podrían requerir los modelos
                    predict_df['pickup_weekday'] = 1  # podríamos ajustar esto
                    
                    # Intentar predecir
                    try:
                        predictions, probabilities = model_utils.predict_airport(predict_df)
                        
                        if predictions is not None:
                            # Mostrar predicción
                            result = "Viaje a Aeropuerto" if predictions[0] == 1 else "Viaje Normal (No a Aeropuerto)"
                            
                            # Color según la predicción
                            result_color = "green" if predictions[0] == 1 else "blue"
                            
                            st.markdown(f"<h3 style='color:{result_color};'>Resultado: {result}</h3>", unsafe_allow_html=True)
                            
                            # Mostrar probabilidad
                            if probabilities is not None:
                                prob_value = probabilities[0] if predictions[0] == 1 else 1 - probabilities[0]
                                st.metric(
                                    label="Confianza de la predicción",
                                    value=f"{prob_value*100:.1f}%"
                                )
                                
                                # Visualizar probabilidad
                                fig = go.Figure(go.Indicator(
                                    mode = "gauge+number",
                                    value = prob_value*100,
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title = {'text': "Confianza (%)"},
                                    gauge = {
                                        'axis': {'range': [None, 100]},
                                        'steps': [
                                            {'range': [0, 30], 'color': "lightgray"},
                                            {'range': [30, 70], 'color': "gray"},
                                            {'range': [70, 100], 'color': result_color}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 4},
                                            'thickness': 0.75,
                                            'value': prob_value*100
                                        }
                                    }
                                ))
                                st.plotly_chart(fig)
                        else:
                            st.error("No se pudo generar una clasificación con los datos proporcionados.")
                    except Exception as e:
                        st.error(f"Error al clasificar: {e}")
            
            # Tab 3: Análisis de Features
            with pred_tabs[2]:
                st.subheader("Importancia de Variables")
                
                # Seleccionar modelo para analizar
                model_for_analysis = st.selectbox(
                    "Seleccionar modelo para analizar",
                    options=[name for name, info in available_models.items() if 'nn' not in name],
                    format_func=lambda x: available_models[x]['type'] if x in available_models else x
                )
                
                if model_for_analysis:
                    # Obtener importancia de features
                    try:
                        importances = model_utils.get_feature_importance(model_for_analysis)
                        
                        if importances:
                            # Convertir a DataFrame para visualización
                            imp_df = pd.DataFrame(
                                {'Feature': list(importances.keys()), 'Importance': list(importances.values())}
                            ).sort_values('Importance', ascending=False).head(15)
                            
                            # Gráfico de barras horizontales
                            fig = px.bar(
                                imp_df,
                                x='Importance',
                                y='Feature',
                                orientation='h',
                                title=f"Top 15 Variables más Importantes para {available_models[model_for_analysis]['type']}",
                                labels={'Importance': 'Importancia Relativa', 'Feature': 'Variable'},
                                color='Importance',
                                color_continuous_scale='Viridis'
                            )
                            
                            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                            st.plotly_chart(fig, width='stretch')
                            
                            # Mostrar tabla con importancias
                            with st.expander("Ver tabla de importancias"):
                                st.table(imp_df)
                        else:
                            st.warning("No se pudieron obtener las importancias de las variables para este modelo.")
                    except Exception as e:
                        st.error(f"Error al analizar la importancia de variables: {e}")
    except Exception as e:
        st.error(f"Error al cargar los módulos de machine learning: {e}")
        st.info("""
        Para usar la funcionalidad de modelos de machine learning:
        1. Asegúrate de tener instaladas las dependencias necesarias (scikit-learn, tensorflow, joblib)
        2. Ejecuta el script train_models.py para entrenar los modelos
        3. Verifica que la carpeta 'models/' existe y contiene los archivos de modelos
        """)

# Footer profesional
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(90deg, #1f4e79 0%, #2e86ab 100%); 
            padding: 2rem 1rem; border-radius: 10px; margin-top: 3rem;
            text-align: center; color: white;">
    <h3 style="margin: 0; color: white;">🚖 NYC Ride-Hailing Analytics Dashboard</h3>
    <p style="margin: 0.5rem 0; opacity: 0.9;">Professional Data Analysis & Predictive Modeling Platform</p>
    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
        <span>📊 Powered by Streamlit & Plotly</span> | 
        <span>🤖 Machine Learning with Scikit-learn & TensorFlow</span> | 
        <span>📈 Real-time Analytics</span>
    </div>
    <div style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;">
        <p>© 2024 NYC Transportation Analytics | Data Source: NYC TLC</p>
        <p>Built with ❤️ for data-driven transportation insights</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Información adicional en sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                border-left: 4px solid #2e86ab; margin: 1rem 0;">
        <h4 style="margin: 0; color: #2e86ab;">💡 Consejos para Capturas</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1rem; font-size: 0.9rem;">
            <li>Usa filtros para datos específicos</li>
            <li>Prueba diferentes pestañas</li>
            <li>Interactúa con los gráficos</li>
            <li>Explora los modelos ML</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de reset
    if st.button("🔄 Reset Dashboard", help="Reinicia todos los filtros"):
        st.experimental_rerun()
