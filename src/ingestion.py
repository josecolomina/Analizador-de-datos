import duckdb
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'data/ecommerce.db'

def create_schema(con: duckdb.DuckDBPyConnection):
    """
    Creates the database schema if it does not exist.

    Args:
        con (duckdb.DuckDBPyConnection): Active DuckDB connection.
    """
    con.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR PRIMARY KEY,
            product_name VARCHAR,
            category VARCHAR,
            price DOUBLE,
            cost DOUBLE
        );
        
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR PRIMARY KEY,
            name VARCHAR,
            email VARCHAR,
            city VARCHAR,
            signup_date DATE
        );
        
        CREATE TABLE IF NOT EXISTS sales (
            order_id VARCHAR PRIMARY KEY,
            date TIMESTAMP,
            customer_id VARCHAR,
            product_id VARCHAR,
            quantity INTEGER,
            total_amount DOUBLE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)
    logger.info("Database schema verified/created.")

def load_data(con: duckdb.DuckDBPyConnection):
    """
    Loads raw data from CSV files into the DuckDB database.

    Args:
        con (duckdb.DuckDBPyConnection): Active DuckDB connection.
    """
    logger.info("Reading CSV files...")
    try:
        products_df = pd.read_csv('data/raw/products.csv')
        customers_df = pd.read_csv('data/raw/customers.csv')
        sales_df = pd.read_csv('data/raw/sales.csv')
        
        logger.info("Inserting data into DuckDB...")
        con.execute("INSERT OR REPLACE INTO products SELECT * FROM products_df")
        con.execute("INSERT OR REPLACE INTO customers SELECT * FROM customers_df")
        con.execute("INSERT OR REPLACE INTO sales SELECT * FROM sales_df")
        
        count_sales = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        logger.info(f"Total sales records in DB: {count_sales}")
        
    except FileNotFoundError as e:
        logger.error(f"Error loading data: {e}")
        raise

def main():
    """
    Main execution function for data ingestion.
    """
    os.makedirs('data', exist_ok=True)
    
    try:
        con = duckdb.connect(DB_PATH)
        create_schema(con)
        load_data(con)
        con.close()
        logger.info("Ingestion process completed successfully.")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise

if __name__ == "__main__":
    main()
