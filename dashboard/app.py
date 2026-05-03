import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os

engine = create_engine("mysql+pymysql://root:jeet1108@localhost/ecommerce_db")

st.title("E-commerce Sales Dashboard")
st.write('Real Time analytics powered by MySQL and Airflow')


@st.cache_data
def load_data():
    orders_df = pd.read_sql("SELECT * FROM orders", engine)
    customers_df = pd.read_sql("SELECT * FROM customers", engine)
    order_items_df = pd.read_sql("SELECT * FROM order_items", engine)
    products_df = pd.read_sql("SELECT * FROM product", engine)

    orders_customers = orders_df.merge(customers_df, on='customer_id', how='left')
    full_df = orders_customers.merge(order_items_df, on='order_id', how='left')
    full_df = full_df.merge(products_df, on='product_id', how='left')

    full_df['order_date'] = pd.to_datetime(full_df['order_date'])
    full_df['month'] = full_df['order_date'].dt.to_period('M').astype(str)

    return full_df

full_df = load_data()


st.sidebar.title("Filters")
st.sidebar.write('E-Commerce Analytics')

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(full_df['category'].dropna().unique().tolist())
)

selected_payment = st.sidebar.multiselect(
    "Select Payment Method",
    full_df['payment_method'].unique().tolist(),
    default=full_df['payment_method'].unique().tolist()
)

selected_device = st.sidebar.multiselect(
    "Select Device Type",
    full_df['device_type'].unique().tolist(),
    default=full_df['device_type'].unique().tolist()
)

selected_status = st.sidebar.multiselect(
    "Select Order Status",
    full_df['order_status'].unique().tolist(),
    default=full_df['order_status'].unique().tolist()
)


filtered_df = full_df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

if selected_payment:
    filtered_df = filtered_df[filtered_df['payment_method'].isin(selected_payment)]

if selected_device:
    filtered_df = filtered_df[filtered_df['device_type'].isin(selected_device)]

if selected_status:
    filtered_df = filtered_df[filtered_df['order_status'].isin(selected_status)]

revenue_by_category = filtered_df.groupby('category')['total_price'].sum().reset_index()
monthly_sale = filtered_df.groupby('month')['total_price'].sum().reset_index()
payment_rev = filtered_df.groupby('payment_method')['total_price'].sum().reset_index()
device_rev = filtered_df.groupby('device_type')['total_price'].sum().reset_index()
traffic_rev = filtered_df.groupby('traffic_source')['total_price'].sum().reset_index()
order_stat = filtered_df.groupby('order_status')['order_id'].count().reset_index()
top_customers = filtered_df.groupby('customer_id')['total_price'].sum().reset_index().nlargest(10, 'total_price')
customer_spending = filtered_df.groupby('customer_id')['total_price'].sum().reset_index()


st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['total_price'].sum()
col1.metric("Total Revenue", f"${total_revenue/1_000_000:.1f}M")
col2.metric("Total Orders", f"{filtered_df['order_id'].nunique():,}")
col3.metric("Top Category", revenue_by_category.loc[revenue_by_category['total_price'].idxmax(), 'category'] if len(revenue_by_category) > 0 else "N/A")
col4.metric("Total Customers", f"{filtered_df['customer_id'].nunique():,}")

st.header("Revenue By Category")
fig = px.bar(revenue_by_category, x='category', y='total_price',
             title='Revenue by Category', color='category')
st.plotly_chart(fig, use_container_width=True)

st.header("Monthly Sale Trend")
fig = px.line(monthly_sale, x='month', y='total_price',
              title='Monthly Sales Trend')
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.header("Revenue By Payment")
    fig = px.pie(payment_rev, values='total_price', names='payment_method',
                 title='Revenue By Payment Method')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Revenue By Device")
    fig = px.pie(device_rev, values='total_price', names='device_type',
                 title='Revenue By Device Type')
    st.plotly_chart(fig, use_container_width=True)

st.header("Order Status Breakdown")
fig = px.bar(order_stat, x='order_status', y='order_id',
             title='Order Status', color='order_status')
st.plotly_chart(fig, use_container_width=True)

st.header("Revenue By Traffic Source")
fig = px.bar(traffic_rev, x='traffic_source', y='total_price',
             title='Revenue By Traffic Source', color='traffic_source')
st.plotly_chart(fig, use_container_width=True)

st.header("Top 10 Customers")
st.dataframe(top_customers, use_container_width=True)

st.header("Customer Spending Analysis")
search = st.text_input("Search Customer ID:")
if search:
    filtered_customer = customer_spending[
        customer_spending['customer_id'].str.contains(search.upper())
    ]
else:
    filtered_customer = customer_spending

st.dataframe(filtered_customer, use_container_width=True)

st.download_button(
    label="Download Report",
    data=revenue_by_category.to_csv(index=False),
    file_name="ecommerce_report.csv",
    mime="text/csv"
)

min_date = full_df['order_date'].min()
max_date = full_df['order_date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['order_date'] >= pd.Timestamp(date_range[0])) &
        (filtered_df['order_date'] <= pd.Timestamp(date_range[1]))
    ]

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
st.header("Machine Learning Insights")

tab1, tab2, tab3 = st.tabs(["Sales Forecast", "Churn Prediction", "Customer Segments"])

with tab1:
    st.subheader("Sales Forecast:")
    col1, col2 = st.columns(2)
    col1.metric("Next month predicted revenue", "$4.4M")
    col2.metric("Model R2 Score:", "0.65")
    st.image(os.path.join(root_path,"ml","sales_forecast.png"))

with tab2:
    st.subheader("Churn Prediction:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Churn Rate:", "60.8%")
    col2.metric("Model Accuracy:","63%")
    col3.metric("At Risk Customers:", "3,035" )
    st.image(os.path.join(root_path,"ml","churn_prediction.png"))

with tab3:
    st.subheader("Customer Segments:")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VIP Customers:","1,726")
    col2.metric("Regular Customers:","3,175")
    col3.metric("At Risk Customers:","3,035")
    col4.metric("Dormant:","1458")
    st.image(os.path.join(root_path,"ml","customer_segments.png"))