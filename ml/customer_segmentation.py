from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


engine = create_engine("mysql+pymysql://root:jeet1108@localhost/ecommerce_db")
print("Connection successful!")

order_df = pd.read_sql("SELECT * FROM orders", engine)
customer_df = pd.read_sql("Select * from customers", engine)


today = datetime.now().date()

customer_stats = order_df.groupby('customer_id').agg(
    total_orders = ('order_id', 'count'),
    total_spent = ('amount', 'sum'),
    avg_order_value = ('amount', 'mean'),
    last_order_date = ('order_date', 'max')
).reset_index()

customer_stats['last_order_date'] = pd.to_datetime(customer_stats['last_order_date'])
customer_stats['days_since_last_order'] = (pd.Timestamp(today) - customer_stats['last_order_date']).dt.days

rfm= customer_stats[['customer_id', 'total_orders', 'total_spent', 'days_since_last_order']]

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['total_orders', 'total_spent', 'days_since_last_order']])

print(f"RFM shape: {rfm.shape}")
print(rfm.head())

inertias = []
k_range = range(2,10)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_range, inertias, marker='o')
plt.title('Elbow Method - Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.tight_layout()
plt.savefig('elbow_curve.png')
plt.show()
print("Elbow curve saved!")   

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm = rfm.copy()
rfm['segment'] = kmeans.fit_predict(rfm_scaled)

segment_analysis = rfm.groupby('segment').agg(
    total_customers = ('customer_id', 'count'),
    total_orders = ('total_orders', 'mean'),
    avg_spent = ('total_spent', 'mean'),
    avg_days_inactive = ('days_since_last_order', 'mean')
).round(2)

print(segment_analysis)
segment_labels = {
    segment_analysis['avg_spent'].idxmax(): 'VIP',
    segment_analysis['avg_spent'].idxmin(): 'Dormant',
}

remaining = [i for i in range(4) if i not in segment_labels]
days_remaining = segment_analysis.loc[remaining,'avg_days_inactive']
segment_labels[days_remaining.idxmin()] = 'Regular'
segment_labels[days_remaining.idxmin()] = 'At Risk'


segment_labels = {
    3: 'VIP',
    0: 'Regular',
    1: 'At-Risk',
    2: 'Dormant'
}
rfm['segment_name'] = rfm['segment'].map(segment_labels)

print("\n NAMED SEGMENTS")
print(rfm.groupby('segment_name').agg(
    total_customers=('customer_id', 'count'),
    avg_orders=('total_orders', 'mean'),
    avg_spent=('total_spent', 'mean'),
    avg_days_inactive=('days_since_last_order', 'mean')
).round(2))

print("Customer Segments:")
print(segment_analysis)


segment_counts = rfm['segment_name'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(segment_counts.values, labels=segment_counts.index, 
        autopct='%1.1f%%', colors=['gold', 'lightblue', 'orange', 'lightcoral'])
plt.title('Customer Segmentation')
plt.savefig('customer_segments.png')
plt.show()
print("Segmentation chart saved!")