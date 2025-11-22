import duckdb
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'data/ecommerce.db'

def process_data():
    """
    Performs data processing and feature engineering.
    Aggregates sales by day and creates lag features for time series forecasting.
    """
    con = duckdb.connect(DB_PATH)
    
    logger.info("Loading raw sales data...")
    # Aggregate sales by day
    query = """
        SELECT 
            date_trunc('day', date) as ds,
            SUM(total_amount) as y
        FROM sales
        GROUP BY 1
        ORDER BY 1
    """
    df = con.execute(query).fetchdf()
    
    logger.info("Generating time series features...")
    # Ensure complete timeline (fill gaps with 0)
    df = df.set_index('ds').asfreq('D').fillna(0).reset_index()
    
    # Feature Engineering
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    df['lag_1'] = df['y'].shift(1)
    df['lag_7'] = df['y'].shift(7)
    df['rolling_mean_7'] = df['y'].rolling(window=7).mean()
    
    # Remove rows with NaN values (due to lags)
    df_clean = df.dropna()
    
    logger.info("Saving processed data to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE daily_sales AS SELECT * FROM df_clean")
    
    logger.info(f"Processing complete. Processed rows: {len(df_clean)}")
    con.close()

if __name__ == "__main__":
    process_data()
