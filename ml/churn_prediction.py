from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import numpy as np


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
customer_stats['is_churned'] = (customer_stats['days_since_last_order'] > 180).astype(int)

customer_stats = customer_stats.merge(customer_df[['customer_id', 'age', 'gender', 'device_type', 'traffic_source']], on='customer_id', how='left')

le = LabelEncoder()
customer_stats['gender_encoded'] = le.fit_transform(customer_stats['gender'])
customer_stats['device_encoded'] = le.fit_transform(customer_stats['device_type'])
customer_stats['traffic_encoded'] = le.fit_transform(customer_stats['traffic_source'])

features = ['total_orders', 'total_spent', 'avg_order_value', 'age', 'gender_encoded', 'device_encoded', 'traffic_encoded']

x = customer_stats[features]
y = customer_stats['is_churned']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(x_train, y_train)
lr_pred = lr_model.predict(x_test)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(x_train, y_train)
rf_pred = rf_model.predict(x_test)

print("Logistic Regression:")
print(f"Accuracy: :{accuracy_score(y_test, lr_pred):.2f}")
print(classification_report(y_test, lr_pred))


print("RandomForest Regressor:")
print(f"Accuracy: :{accuracy_score(y_test, rf_pred):.2f}")
print(classification_report(y_test, rf_pred))

print(f"Total customers: {len(customer_stats)}")
print(f"Churned customers: {customer_stats['is_churned'].sum()}")
print(f"Active customers: {(customer_stats['is_churned']==0).sum()}")
print(f"Churn rate: {customer_stats['is_churned'].mean()*100:.1f}%")
print(customer_stats.head())

feature_importance = pd.DataFrame({
    'feature' : features,
    'importance' : rf_model.feature_importances_
}).sort_values('importance', ascending = False)

print("Feature Importance:")
print(feature_importance)

plt.figure(figsize=(10,6))
plt.barh(feature_importance['feature'], feature_importance['importance'])
plt.title("Feature Importance- Churn Prediction")
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig('churn_prediction.png')
plt.show()
print('Chart Saved!')