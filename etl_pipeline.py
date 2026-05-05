import pandas as pd

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:jeet1108@localhost/ecommerce_db")

import tempfile
import os
from s3_utils import upload_file

print("Connection successful!")

customer_df = pd.read_sql("SELECT * FROM customers", engine)


order_df = pd.read_sql("SELECT * FROM orders", engine)

product_df = pd.read_sql("SELECT * FROM product", engine)

order_items_df = pd.read_sql("SELECT * FROM order_items", engine)

print(f"Customers: {customer_df.shape}")
print(f"Orders: {order_df.shape}")
print(f"Products: {product_df.shape}")
print(f"Order_items: {order_items_df.shape}")


order_customers = order_df.merge(customer_df, on='customer_id', how="left")

merge_df = order_customers.merge(order_items_df, on='order_id', how='left')

merge_df = merge_df.merge(product_df, on='product_id', how='left')

revenue_by_category = merge_df.groupby('category')['total_price'].sum().reset_index()

customer_spending = merge_df.groupby('customer_id')['total_price'].sum().reset_index()

top_ten_customers = customer_spending.nlargest(10,'total_price')

merge_df['order_date'] = pd.to_datetime(merge_df['order_date'])
merge_df['month'] = merge_df['order_date'].dt.to_period('M')
monthly_sale = merge_df.groupby('month')['total_price'].sum().reset_index()

payment_revenue = merge_df.groupby('payment_method')['total_price'].sum().reset_index()

print(f"order_customers: {order_customers}")
print(f"merge_df: {merge_df}")
print(f"merge_df: {merge_df}")
print(f"revenue_by_category: {revenue_by_category}")
print(f"Top_ten_Customer {top_ten_customers}")
print(f"Monthly sale {monthly_sale}")
print(f"Revenue_By_Payment {payment_revenue}")

revenue_by_category.to_sql('report_revenue_by_category', engine, if_exists='replace', index=False)
print("Revenue By Category Loaded!")

customer_spending.to_sql('report_customer_spending', engine, if_exists='replace', index=False)
print("Customer_Spending Loaded!")

top_ten_customers.to_sql('report_top_ten_customers', engine, if_exists='replace', index=False)
print("Top_ten_Customers Loaded!")


monthly_sale.to_sql('report_monthly_sale', engine, if_exists='replace', index=False)
print("Monthly_Sale Loaded!")


payment_revenue.to_sql('report_payment_revenue', engine, if_exists='replace', index=False)
print("Payment_Revenue Loaded!")

print("Uploading reports to S3...")
temp_dir = tempfile.gettempdir()

# Save to temp directory
revenue_by_category.to_csv(os.path.join(temp_dir, 'revenue_by_category.csv'), index=False)
customer_spending.to_csv(os.path.join(temp_dir, 'customer_spending.csv'), index=False)
top_ten_customers.to_csv(os.path.join(temp_dir, 'top_ten_customers.csv'), index=False)
monthly_sale.to_csv(os.path.join(temp_dir, 'monthly_sale.csv'), index=False)
payment_revenue.to_csv(os.path.join(temp_dir, 'payment_revenue.csv'), index=False)

# Upload to S3
upload_file(os.path.join(temp_dir, 'revenue_by_category.csv'), 'reports/revenue_by_category.csv')
upload_file(os.path.join(temp_dir, 'customer_spending.csv'), 'reports/customer_spending.csv')
upload_file(os.path.join(temp_dir, 'top_ten_customers.csv'), 'reports/top_ten_customers.csv')
upload_file(os.path.join(temp_dir, 'monthly_sale.csv'), 'reports/monthly_sale.csv')
upload_file(os.path.join(temp_dir, 'payment_revenue.csv'), 'reports/payment_revenue.csv')
print("All reports uploaded to S3!")