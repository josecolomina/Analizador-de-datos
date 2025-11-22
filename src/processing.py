import duckdb
import pandas as pd
import numpy as np

DB_PATH = 'data/ecommerce.db'

def process_data():
    con = duckdb.connect(DB_PATH)
    
    print("Cargando datos crudos...")
    # Agregar ventas por día
    query = """
        SELECT 
            date_trunc('day', date) as ds,
            SUM(total_amount) as y
        FROM sales
        GROUP BY 1
        ORDER BY 1
    """
    df = con.execute(query).fetchdf()
    
    print("Generando features...")
    # Asegurar que tenemos todas las fechas (rellenar huecos con 0)
    df = df.set_index('ds').asfreq('D').fillna(0).reset_index()
    
    # Feature Engineering para ML (Lag features)
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    df['lag_1'] = df['y'].shift(1)
    df['lag_7'] = df['y'].shift(7)
    df['rolling_mean_7'] = df['y'].rolling(window=7).mean()
    
    # Eliminar filas con NaNs (primeros días)
    df_clean = df.dropna()
    
    # Guardar tabla procesada
    print("Guardando datos procesados en DuckDB...")
    con.execute("CREATE OR REPLACE TABLE daily_sales AS SELECT * FROM df_clean")
    
    print(f"Datos procesados guardados. Filas: {len(df_clean)}")
    con.close()

if __name__ == "__main__":
    process_data()
