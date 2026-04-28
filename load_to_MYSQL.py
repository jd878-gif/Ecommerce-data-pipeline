import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

print("Connection successful!")

customer_df = pd.read_csv('data/customer.csv')
order_df = pd.read_csv('data/order.csv')
product_df = pd.read_csv('data/product.csv')
order_items_df = pd.read_csv('data/order_items.csv')

customer_df.to_sql('customers', engine, if_exists='replace', index=False)
print("Customers loaded!")

order_df.to_sql('orders', engine, if_exists='replace', index=False)
print("orders loaded!")

product_df.to_sql('product', engine, if_exists='replace',index=False)
print("products loaded!")

order_items_df.to_sql('order_items', engine, if_exists='replace', index=False)
print("order_items loaded!")