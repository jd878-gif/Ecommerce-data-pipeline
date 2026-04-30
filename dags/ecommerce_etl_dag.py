from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import create_engine

default_args = {
    'owner' : 'jeet',
    'retries' : 1,
    'retry_delay' : timedelta(minutes=3),
    'email_on_failure' : False
}


DB_URL = "mysql+pymysql://root:jeet1108@host.docker.internal/ecommerce_db"

def extract(**context):
        print("extract starting..")
        engine = create_engine(DB_URL)

        customer_df = pd.read_sql("Select * from customers", engine)
        order_df = pd.read_sql("Select * from orders", engine)
        product_df = pd.read_sql("Select * From product", engine)
        order_items_df = pd.read_sql("Select * From order_items", engine)

        context['ti'].xcom_push(key='customers', value=customer_df.to_json())
        context['ti'].xcom_push(key='orders', value=order_df.to_json())
        context['ti'].xcom_push(key='product', value=product_df.to_json())
        context['ti'].xcom_push(key='order_items', value=order_items_df.to_json())
        return "extracted successfully"


def transform(**context):
    print("Transforming started..")
    customer_json = context['ti'].xcom_pull(task_ids = 'extract_data', key = 'customers')
    order_json = context['ti'].xcom_pull(task_ids = 'extract_data', key = 'orders')
    product_json = context['ti'].xcom_pull(task_ids = 'extract_data', key = 'product')
    order_items_json = context['ti'].xcom_pull(task_ids = 'extract_data', key = 'order_items')

    customer_df = pd.read_json(customer_json)
    order_df = pd.read_json(order_json)
    product_df = pd.read_json(product_json)
    order_items_df = pd.read_json(order_items_json) 

    order_customers = order_df.merge(customer_df, on='customer_id', how="left")
    result_df = order_customers.merge(order_items_df, on='order_id', how='left')
    result_df = result_df.merge(product_df, on='product_id', how='left')

    result_df['order_date'] = pd.to_datetime(result_df['order_date'])
    result_df['month'] = result_df['order_date'].dt.to_period('M').astype(str)

    revenue_by_category = result_df.groupby('category')['total_price'].sum().reset_index()
    customer_spending = result_df.groupby('customer_id')['total_price'].sum().reset_index()
    top_ten_customers = customer_spending.nlargest(10,'total_price')
    monthly_sale = result_df.groupby('month')['total_price'].sum().reset_index()
    payment_revenue = result_df.groupby('payment_method')['total_price'].sum().reset_index()
    device_revenue = result_df.groupby('device_type')['total_price'].sum().reset_index()
    traffic_revenue = result_df.groupby('traffic_source')['total_price'].sum().reset_index()
    order_status = result_df.groupby('order_status')['order_id'].count().reset_index()

    
    context['ti'].xcom_push(key='revenue_by_category', value=revenue_by_category.to_json())
    context['ti'].xcom_push(key = 'customer_spending', value = customer_spending.to_json())
    context['ti'].xcom_push(key='top_ten_customers', value=top_ten_customers.to_json())
    context['ti'].xcom_push(key='monthly_sale', value=monthly_sale.to_json())
    context['ti'].xcom_push(key='payment_revenue', value=payment_revenue.to_json())
    context['ti'].xcom_push(key='device_revenue', value=device_revenue.to_json())
    context['ti'].xcom_push(key='traffic_revenue', value=traffic_revenue.to_json())  
    context['ti'].xcom_push(key='order_status', value=order_status.to_json()) 
    return "Transformed successfully"

    
def load(**context):
    print("Loading started..")
    engine = create_engine(DB_URL)

    revenue_by_category = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'revenue_by_category'))
    customer_spending = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'customer_spending'))
    top_ten_customers = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'top_ten_customers'))
    
    monthly_sale = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'monthly_sale'))
    
    payment_revenue = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'payment_revenue'))
    
    device_revenue = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'device_revenue'))
    
    traffic_revenue = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'traffic_revenue'))

    order_status = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'order_status'))


    revenue_by_category.to_sql('report_revenue_by_category', engine, if_exists='append', index=False)
    customer_spending.to_sql('customer_spending',  engine, if_exists='append', index=False)
    top_ten_customers.to_sql('top_ten_customers', engine, if_exists='append', index=False)
    monthly_sale.to_sql('monthly_sale', engine, if_exists='append', index=False)
    payment_revenue.to_sql('payment_revenue', engine, if_exists='append', index=False)
    device_revenue.to_sql('device_revenue', engine, if_exists='append', index=False)
    traffic_revenue.to_sql('traffic_revenue', engine, if_exists='append', index=False)
    order_status.to_sql('order_stauts', engine, if_exists='append', index=False)
    print("Revenue_by_Category Loaded!")
    print("customer_spending Loaded!")
    print("top_ten_customers Loaded!")
    print("monthly_saleLoaded!")
    print("Payment_revenue Loaded!")
    print("Device_revenue Loaded!")
    print("Traffic_revenue Loaded!")
    print("Order_status Loaded!")


    return "loaded successfully"

    
def summary(**context):
    print("Summary:")

    revenue_by_category = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'revenue_by_category'))
    customer_spending = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'customer_spending'))
    top_ten_customers = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'top_ten_customers'))
    monthly_sale = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'monthly_sale'))
    payment_revenue = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'payment_revenue'))
    device_revenue = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'device_revenue'))
    traffic_revenue = pd .read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'traffic_revenue'))
    order_status = pd.read_json(context['ti'].xcom_pull(task_ids = 'transform_data', key = 'order_status'))

    print(f"Total categories: {len(revenue_by_category)}")
    print(f"Highest revenue category: {revenue_by_category.loc[revenue_by_category['total_price'].idxmax(), 'category']}")

    print(f"Top spender: {top_ten_customers.iloc[0]['customer_id']}")
    print(f"Top spender amount: {top_ten_customers.iloc[0]['total_price']}")

    print(f"Best month: {monthly_sale.loc[monthly_sale['total_price'].idxmax(), 'month']}")
    print(f"Customer Top Spending: {customer_spending.iloc[0]['customer_id']}")
    print(f"Most Popular Payment: {payment_revenue.loc[payment_revenue['total_price'].idxmax(), 'payment_method']}")
    print(f"Most Popular Device: {device_revenue.loc[device_revenue['total_price'].idxmax(), 'device_type']}")
    print(f"Top Traffic Source: {traffic_revenue.loc[traffic_revenue['total_price'].idxmax(), 'traffic_source']} ")
    print(f"Most common Order Status: {order_status.loc[order_status['order_id'].idxmax(), 'order_status']}")
    return "Summary completed successfully"


with DAG(
    dag_id='ecommerce_etl_dag',
    default_args=default_args,
    description='My First Dag',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False
)as dag:
     
     extract_task = PythonOperator(
        task_id = 'extract_data',
        python_callable=extract
       
    )
     
     transform_task = PythonOperator(
          task_id = 'transform_data',
          python_callable=transform
          
     )

     load_task = PythonOperator(
          task_id = 'load_data',
          python_callable=load
          
     )

     summary_task = PythonOperator(
          task_id = 'summary_data',
          python_callable=summary
          
     )

     extract_task >> transform_task >> load_task >> summary_task


 

