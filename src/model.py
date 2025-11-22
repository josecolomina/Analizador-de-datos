import duckdb
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'data/ecommerce.db'

def train_and_predict():
    """
    Trains a Random Forest model on daily sales data and generates a 30-day forecast.
    """
    con = duckdb.connect(DB_PATH)
    
    logger.info("Loading processed data...")
    df = con.execute("SELECT * FROM daily_sales ORDER BY ds").fetchdf()
    
    # Prepare features and target
    features = ['day_of_week', 'month', 'lag_1', 'lag_7', 'rolling_mean_7']
    target = 'y'
    
    # Train/Test Split (last 30 days for validation)
    train_size = int(len(df) * 0.9)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]
    
    X_train = train[features]
    y_train = train[target]
    X_test = test[features]
    y_test = test[target]
    
    logger.info("Training RandomForest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    logger.info(f"Model Performance - MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    
    # --- Future Forecasting (30 days) ---
    logger.info("Generating 30-day forecast...")
    
    last_date = df['ds'].max()
    future_dates = [last_date + timedelta(days=x) for x in range(1, 31)]
    
    # Recursive forecasting
    future_predictions = []
    history = df['y'].tolist()
    
    for date in future_dates:
        # Construct features for the current prediction date
        feat = {
            'day_of_week': date.dayofweek,
            'month': date.month,
            'lag_1': history[-1],
            'lag_7': history[-7],
            'rolling_mean_7': np.mean(history[-7:])
        }
        
        # Predict
        X_future = pd.DataFrame([feat])
        pred = model.predict(X_future)[0]
        
        # Append prediction to history for next iteration
        future_predictions.append({
            'ds': date,
            'y_pred': pred,
            'type': 'forecast'
        })
        history.append(pred)
    
    forecast_df = pd.DataFrame(future_predictions)
    
    # Combine history and forecast for storage
    history_df = df[['ds', 'y']].rename(columns={'y': 'y_pred'})
    history_df['type'] = 'history'
    
    final_df = pd.concat([history_df, forecast_df])
    
    logger.info("Saving forecasts to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE forecasts AS SELECT * FROM final_df")
    con.close()
    logger.info("Modeling and forecasting completed successfully.")

if __name__ == "__main__":
    train_and_predict()
