import duckdb
import pandas as pd
import os

DB_PATH = 'data/ecommerce.db'

def create_schema(con):
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
    print("Esquema creado/verificado.")

def load_data(con):
    # Usar Pandas para leer CSVs (como solicitado)
    print("Leyendo CSVs con Pandas...")
    products_df = pd.read_csv('data/raw/products.csv')
    customers_df = pd.read_csv('data/raw/customers.csv')
    sales_df = pd.read_csv('data/raw/sales.csv')
    
    # DuckDB puede ingerir DataFrames directamente
    print("Insertando datos en DuckDB...")
    con.execute("INSERT OR REPLACE INTO products SELECT * FROM products_df")
    con.execute("INSERT OR REPLACE INTO customers SELECT * FROM customers_df")
    con.execute("INSERT OR REPLACE INTO sales SELECT * FROM sales_df")
    
    # Verificar conteos
    count_sales = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    print(f"Total de ventas en DB: {count_sales}")

def main():
    os.makedirs('data', exist_ok=True)
    con = duckdb.connect(DB_PATH)
    
    create_schema(con)
    load_data(con)
    
    con.close()
    print("Ingesta completada.")

if __name__ == "__main__":
    main()
