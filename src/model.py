import duckdb
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import timedelta

DB_PATH = 'data/ecommerce.db'

def train_and_predict():
    con = duckdb.connect(DB_PATH)
    
    print("Cargando datos procesados...")
    df = con.execute("SELECT * FROM daily_sales ORDER BY ds").fetchdf()
    
    # Preparar datos para sklearn
    features = ['day_of_week', 'month', 'lag_1', 'lag_7', 'rolling_mean_7']
    target = 'y'
    
    # Split Train/Test (últimos 30 días para test)
    train_size = int(len(df) * 0.9)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]
    
    X_train = train[features]
    y_train = train[target]
    X_test = test[features]
    y_test = test[target]
    
    print("Entrenando modelo RandomForest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluar
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"Métricas del modelo - MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    
    # --- Generar Predicciones Futuras (30 días) ---
    print("Generando forecast para los próximos 30 días...")
    
    last_date = df['ds'].max()
    future_dates = [last_date + timedelta(days=x) for x in range(1, 31)]
    
    # Necesitamos generar features iterativamente porque dependen de lags
    # Para simplificar en este demo, usaremos una aproximación recursiva simple
    
    current_row = df.iloc[-1].copy()
    future_predictions = []
    
    # Buffer de historia reciente para calcular lags y rolling
    history = df['y'].tolist()
    
    for date in future_dates:
        # Construir features para hoy
        feat = {
            'day_of_week': date.dayofweek,
            'month': date.month,
            'lag_1': history[-1],
            'lag_7': history[-7],
            'rolling_mean_7': np.mean(history[-7:])
        }
        
        # Predecir
        X_future = pd.DataFrame([feat])
        pred = model.predict(X_future)[0]
        
        # Guardar y actualizar historia
        future_predictions.append({
            'ds': date,
            'y_pred': pred,
            'type': 'forecast'
        })
        history.append(pred)
    
    forecast_df = pd.DataFrame(future_predictions)
    
    # Guardar en DB
    # Unimos históricos (type='history') con forecast
    history_df = df[['ds', 'y']].rename(columns={'y': 'y_pred'})
    history_df['type'] = 'history'
    
    final_df = pd.concat([history_df, forecast_df])
    
    print("Guardando predicciones en DuckDB...")
    con.execute("CREATE OR REPLACE TABLE forecasts AS SELECT * FROM final_df")
    con.close()
    print("Modelado completado.")

if __name__ == "__main__":
    train_and_predict()
