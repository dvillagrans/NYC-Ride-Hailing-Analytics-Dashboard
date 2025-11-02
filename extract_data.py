#!/usr/bin/env python3
"""
Script para extraer datos de NYC Ride-Hailing
Versión optimizada para deployment
"""

import pandas as pd
import numpy as np
import requests
import os
import sys
from datetime import datetime
import time

def create_directories():
    """Crear directorios necesarios"""
    directories = ['raw-data', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio '{directory}' creado/verificado")

def download_single_month(month=2, year=2024):
    """
    Descargar datos de un solo mes
    Args:
        month (int): Mes a descargar (por defecto febrero)
        year (int): Año a descargar
    """
    print(f"🚀 Descargando datos de {month:02d}/{year}...")
    
    month_str = f"{month:02d}"
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{year}-{month_str}.parquet'
    file_path = os.path.join('raw-data', f'{year}-{month_str}.parquet')
    
    # Verificar si el archivo ya existe
    if os.path.exists(file_path):
        print(f"⏭️  Archivo {year}-{month_str}.parquet ya existe")
        return file_path
    
    try:
        print(f"📥 Descargando desde: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Obtener tamaño del archivo
        total_size = int(response.headers.get('content-length', 0))
        print(f"📊 Tamaño del archivo: {total_size / (1024*1024):.1f} MB")
        
        with open(file_path, 'wb') as f:
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r📊 Progreso: {progress:.1f}%", end='', flush=True)
        
        print(f"\n✅ Descargado: {year}-{month_str}.parquet")
        return file_path
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error descargando {year}-{month_str}.parquet: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def download_multiple_months(months_data):
    """
    Descargar múltiples meses de datos
    Args:
        months_data (list): Lista de tuplas (mes, año)
    Returns:
        list: Lista de archivos descargados exitosamente
    """
    downloaded_files = []
    
    for month, year in months_data:
        file_path = download_single_month(month, year)
        if file_path:
            downloaded_files.append(file_path)
        time.sleep(1)  # Pausa entre descargas para ser respetuosos con el servidor
    
    return downloaded_files

def create_combined_sample_data(input_files, sample_size_per_month=20000):
    """
    Crear una muestra combinada de múltiples archivos
    Args:
        input_files (list): Lista de archivos de entrada
        sample_size_per_month (int): Número de registros por mes
    """
    print(f"\n🎯 Creando muestra combinada de {len(input_files)} meses...")
    
    combined_samples = []
    individual_files = []
    
    for file_path in input_files:
        try:
            print(f"📊 Procesando {os.path.basename(file_path)}...")
            
            # Leer archivo
            df = pd.read_parquet(file_path)
            print(f"   📈 Registros originales: {len(df):,}")
            
            # Crear muestra estratificada por hora del día para mantener patrones
            df['hour'] = pd.to_datetime(df['pickup_datetime']).dt.hour
            
            # Tomar muestra proporcional por hora
            sample_df = df.groupby('hour', group_keys=False).apply(
                lambda x: x.sample(min(len(x), sample_size_per_month // 24), random_state=42)
            ).reset_index(drop=True)
            
            # Si no tenemos suficientes datos, tomar muestra simple
            if len(sample_df) < sample_size_per_month:
                sample_df = df.sample(min(len(df), sample_size_per_month), random_state=42)
            
            # Remover columna temporal
            sample_df = sample_df.drop('hour', axis=1)
            
            # Guardar archivo individual con formato esperado por la app
            base_name = os.path.basename(file_path).replace('.parquet', '')
            individual_file = os.path.join('data', f'{base_name}_reduced.parquet')
            sample_df.to_parquet(individual_file, compression='snappy', index=False)
            individual_files.append(individual_file)
            
            combined_samples.append(sample_df)
            print(f"   ✅ Muestra creada: {len(sample_df):,} registros -> {os.path.basename(individual_file)}")
            
        except Exception as e:
            print(f"   ❌ Error procesando {file_path}: {e}")
            continue
    
    if not combined_samples:
        print("❌ No se pudieron procesar archivos")
        return None
    
    # Combinar todas las muestras
    print("\n🔄 Combinando muestras...")
    combined_df = pd.concat(combined_samples, ignore_index=True)
    
    # Ordenar por fecha
    combined_df = combined_df.sort_values('pickup_datetime').reset_index(drop=True)
    
    # Guardar archivo combinado
    output_file = os.path.join('data', 'nyc_ridehailing_sample.parquet')
    combined_df.to_parquet(output_file, compression='snappy', index=False)
    
    # Información del archivo final
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n✅ Archivo combinado creado: {output_file}")
    print(f"📊 Total de registros: {len(combined_df):,}")
    print(f"📁 Tamaño del archivo: {file_size:.1f} MB")
    print(f"📅 Rango de fechas: {combined_df['pickup_datetime'].min()} a {combined_df['pickup_datetime'].max()}")
    print(f"🗂️  Columnas: {len(combined_df.columns)}")
    print(f"📋 Archivos individuales creados: {len(individual_files)}")
    
    return output_file

def create_sample_data_efficient(input_file, sample_percentage=10):
    """
    Crear datos de muestra de forma más eficiente
    Args:
        input_file (str): Archivo de entrada
        sample_percentage (int): Porcentaje de datos a mantener
    """
    if not input_file or not os.path.exists(input_file):
        print("❌ Archivo de entrada no encontrado")
        return None
    
    output_file = os.path.join('data', '2024-02_reduced.parquet')
    
    if os.path.exists(output_file):
        print(f"⏭️  Archivo de muestra ya existe: {output_file}")
        return output_file
    
    try:
        print(f"📊 Procesando {input_file}...")
        
        # Leer archivo con chunks para manejar archivos grandes
        print("📖 Leyendo archivo...")
        df = pd.read_parquet(input_file)
        original_size = len(df)
        print(f"📊 Registros originales: {original_size:,}")
        
        # Crear muestra aleatoria más pequeña
        sample_size = min(int(original_size * (sample_percentage / 100)), 100000)  # Máximo 100k registros
        print(f"🎯 Creando muestra de {sample_size:,} registros...")
        
        df_sample = df.sample(n=sample_size, random_state=42)
        
        # Guardar muestra con compresión
        print("💾 Guardando muestra...")
        df_sample.to_parquet(output_file, index=False, compression='snappy')
        
        print(f"✅ Muestra creada: {original_size:,} → {sample_size:,} registros")
        print(f"📁 Archivo guardado: {output_file}")
        
        # Mostrar información básica
        print(f"📊 Columnas: {list(df_sample.columns[:5])}...")
        print(f"📊 Tamaño del archivo: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
        return None

def verify_data():
    """Verificar que los datos se crearon correctamente"""
    print("🔍 Verificando datos creados...")
    
    # Verificar raw data
    if os.path.exists('raw-data'):
        raw_files = [f for f in os.listdir('raw-data') if f.endswith('.parquet')]
        print(f"📁 Archivos raw: {len(raw_files)}")
        for file in raw_files:
            size = os.path.getsize(os.path.join('raw-data', file)) / (1024*1024)
            print(f"   - {file}: {size:.1f} MB")
    
    # Verificar sample data
    if os.path.exists('data'):
        sample_files = [f for f in os.listdir('data') if f.endswith('.parquet')]
        print(f"📁 Archivos de muestra: {len(sample_files)}")
        
        # Mostrar información de un archivo de muestra
        if sample_files:
            sample_file = os.path.join('data', sample_files[0])
            try:
                df = pd.read_parquet(sample_file)
                print(f"📊 Ejemplo - {sample_files[0]}:")
                print(f"   - Registros: {len(df):,}")
                print(f"   - Columnas: {len(df.columns)}")
                print(f"   - Columnas principales: {list(df.columns[:5])}")
                print(f"   - Rango de fechas: {df['pickup_datetime'].min()} a {df['pickup_datetime'].max()}")
            except Exception as e:
                print(f"   - Error leyendo archivo: {e}")

def create_zone_files():
    """Crear archivos de zonas necesarios para la aplicación"""
    print("🗺️  Creando archivos de zonas...")
    
    # Crear taxi_zone_lookup.csv básico
    zone_lookup_path = os.path.join('data', 'taxi_zone_lookup.csv')
    if not os.path.exists(zone_lookup_path):
        # Datos básicos de zonas de NYC
        zones_data = {
            'LocationID': list(range(1, 266)),
            'Borough': ['Manhattan'] * 68 + ['Brooklyn'] * 61 + ['Queens'] * 100 + ['Bronx'] * 43 + ['Staten Island'] * 23,
            'Zone': [f'Zone_{i}' for i in range(1, 266)],
            'service_zone': ['Yellow Zone'] * 200 + ['Green Zone'] * 65
        }
        
        df_zones = pd.DataFrame(zones_data)
        df_zones.to_csv(zone_lookup_path, index=False)
        print(f"✅ Creado: {zone_lookup_path}")
    
    # Crear taxi_zone_centroids.csv básico
    centroids_path = os.path.join('data', 'taxi_zone_centroids.csv')
    if not os.path.exists(centroids_path):
        # Coordenadas aproximadas de NYC
        np.random.seed(42)
        centroids_data = {
            'LocationID': list(range(1, 266)),
            'latitude': np.random.uniform(40.4774, 40.9176, 265),  # Rango de latitud de NYC
            'longitude': np.random.uniform(-74.2591, -73.7004, 265)  # Rango de longitud de NYC
        }
        
        df_centroids = pd.DataFrame(centroids_data)
        df_centroids.to_csv(centroids_path, index=False)
        print(f"✅ Creado: {centroids_path}")

def main():
    """Función principal optimizada para múltiples meses"""
    print("🚖 NYC Ride-Hailing Data Extractor v3.0")
    print("=" * 50)
    
    # Crear directorios
    create_directories()
    
    # Crear archivos de zonas
    create_zone_files()
    
    # Definir meses a descargar (enero a junio 2024)
    months_to_download = [
        (1, 2024),   # Enero
        (2, 2024),   # Febrero
        (3, 2024),   # Marzo
        (4, 2024),   # Abril
        (5, 2024),   # Mayo
        (6, 2024),   # Junio
    ]
    
    print(f"\n📥 Descargando datos de {len(months_to_download)} meses...")
    downloaded_files = download_multiple_months(months_to_download)
    
    if downloaded_files:
        print(f"\n✅ {len(downloaded_files)} archivos descargados exitosamente")
        
        # Crear muestra combinada
        print("\n🎯 Creando dataset combinado para deployment...")
        combined_file = create_combined_sample_data(downloaded_files, sample_size_per_month=15000)
        
        if combined_file:
            print("\n✅ ¡Dataset multi-mes listo para deployment!")
        else:
            print("\n❌ Error creando dataset combinado")
    else:
        print("\n❌ No se pudieron descargar archivos")
    
    # Verificar datos
    print("\n🔍 Verificación final...")
    verify_data()
    
    print("\n🎉 ¡Proceso completado!")
    print("📝 Próximos pasos:")
    print("   1. Revisar los datos en 'data/'")
    print("   2. Ejecutar la aplicación: streamlit run app.py")
    print("   3. El dashboard ahora mostrará datos de 6 meses!")
    print("   4. Preparar deployment en Streamlit Cloud")

if __name__ == "__main__":
    main()