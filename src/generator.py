import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
LOCALE = 'es_ES'
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 200
HISTORY_YEARS = 2

def generate_products(n: int = NUM_PRODUCTS) -> pd.DataFrame:
    """
    Generates a synthetic dataset of products.

    Args:
        n (int): Number of products to generate.

    Returns:
        pd.DataFrame: DataFrame containing product details.
    """
    fake = Faker(LOCALE)
    products = []
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Juguetes', 'Libros']
    
    for _ in range(n):
        products.append({
            'product_id': fake.uuid4(),
            'product_name': f"{fake.word().capitalize()} {fake.word()}",
            'category': random.choice(categories),
            'price': round(random.uniform(10, 500), 2),
            'cost': round(random.uniform(5, 300), 2)
        })
    return pd.DataFrame(products)

def generate_customers(n: int = NUM_CUSTOMERS) -> pd.DataFrame:
    """
    Generates a synthetic dataset of customers.

    Args:
        n (int): Number of customers to generate.

    Returns:
        pd.DataFrame: DataFrame containing customer details.
    """
    fake = Faker(LOCALE)
    customers = []
    
    for _ in range(n):
        customers.append({
            'customer_id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'city': fake.city(),
            'signup_date': fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(customers)

def generate_sales(products_df: pd.DataFrame, customers_df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Generates synthetic sales history with seasonality and trends.

    Args:
        products_df (pd.DataFrame): DataFrame of available products.
        customers_df (pd.DataFrame): DataFrame of registered customers.
        start_date (datetime): Start date for the sales history.
        end_date (datetime): End date for the sales history.

    Returns:
        pd.DataFrame: DataFrame containing sales transactions.
    """
    fake = Faker(LOCALE)
    sales = []
    current_date = start_date
    
    while current_date <= end_date:
        # Simulate weekend spikes
        is_weekend = current_date.weekday() >= 5
        daily_orders = random.randint(20, 50) if is_weekend else random.randint(10, 30)
        
        # Simulate seasonal spike (December)
        if current_date.month == 12:
            daily_orders = int(daily_orders * 1.5)
            
        for _ in range(daily_orders):
            product = products_df.sample(1).iloc[0]
            customer = customers_df.sample(1).iloc[0]
            quantity = random.randint(1, 5)
            
            sales.append({
                'order_id': fake.uuid4(),
                'date': current_date,
                'customer_id': customer['customer_id'],
                'product_id': product['product_id'],
                'quantity': quantity,
                'total_amount': round(product['price'] * quantity, 2)
            })
        
        current_date += timedelta(days=1)
        
    return pd.DataFrame(sales)

def main():
    """
    Main execution function for data generation.
    """
    logger.info("Generating master data...")
    products_df = generate_products()
    customers_df = generate_customers()
    
    start_date = datetime.now() - timedelta(days=365 * HISTORY_YEARS)
    end_date = datetime.now()
    
    logger.info("Generating sales history...")
    sales_df = generate_sales(products_df, customers_df, start_date, end_date)
    
    # Save data
    os.makedirs('data/raw', exist_ok=True)
    products_df.to_csv('data/raw/products.csv', index=False)
    customers_df.to_csv('data/raw/customers.csv', index=False)
    sales_df.to_csv('data/raw/sales.csv', index=False)
    
    logger.info("Data generation completed successfully.")
    logger.info(f"Products: {len(products_df)}")
    logger.info(f"Customers: {len(customers_df)}")
    logger.info(f"Sales: {len(sales_df)}")

if __name__ == "__main__":
    main()
