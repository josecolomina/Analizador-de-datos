import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Configuración
fake = Faker('es_ES')
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 200
START_DATE = datetime.now() - timedelta(days=365*2) # 2 años de historia
END_DATE = datetime.now()

def generate_products(n=NUM_PRODUCTS):
    products = []
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Juguetes', 'Libros']
    for _ in range(n):
        products.append({
            'product_id': fake.uuid4(),
            'product_name': fake.word().capitalize() + " " + fake.word(),
            'category': random.choice(categories),
            'price': round(random.uniform(10, 500), 2),
            'cost': round(random.uniform(5, 300), 2)
        })
    return pd.DataFrame(products)

def generate_customers(n=NUM_CUSTOMERS):
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

def generate_sales(products_df, customers_df, start_date, end_date):
    sales = []
    current_date = start_date
    
    # Simular estacionalidad y tendencia
    while current_date <= end_date:
        # Más ventas en fin de semana
        is_weekend = current_date.weekday() >= 5
        daily_orders = random.randint(10, 30) if not is_weekend else random.randint(20, 50)
        
        # Estacionalidad simple (más ventas en diciembre)
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
    print("Generando datos maestros...")
    products_df = generate_products()
    customers_df = generate_customers()
    
    print("Generando historial de ventas (esto puede tardar un poco)...")
    sales_df = generate_sales(products_df, customers_df, START_DATE, END_DATE)
    
    # Guardar datos
    os.makedirs('data/raw', exist_ok=True)
    products_df.to_csv('data/raw/products.csv', index=False)
    customers_df.to_csv('data/raw/customers.csv', index=False)
    sales_df.to_csv('data/raw/sales.csv', index=False)
    
    print(f"Datos generados exitosamente en data/raw/")
    print(f" - Productos: {len(products_df)}")
    print(f" - Clientes: {len(customers_df)}")
    print(f" - Ventas: {len(sales_df)}")

if __name__ == "__main__":
    main()
