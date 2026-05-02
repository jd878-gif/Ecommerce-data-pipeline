from sqlalchemy import create_engine
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

engine = create_engine("mysql+pymysql://root:jeet1108@localhost/ecommerce_db")
print("Connection successful!")

# ============================================================
# EXTRACT DATA
# ============================================================
order_df = pd.read_sql("SELECT * FROM orders", engine)

# ============================================================
# FEATURE ENGINEERING
# ============================================================
order_df['order_date'] = pd.to_datetime(order_df['order_date'])
order_df['month'] = order_df['order_date'].dt.to_period('M').astype(str)

# Monthly revenue from orders.amount (has trend!)
monthly_revenue = order_df.groupby('month')['amount'].sum().reset_index()
monthly_revenue.columns = ['month', 'total_price']
monthly_revenue = monthly_revenue.sort_values('month').reset_index(drop=True)

print(f"Monthly Revenue:\n{monthly_revenue}")

# Add features
monthly_revenue['month_num'] = range(1, len(monthly_revenue) + 1)
monthly_revenue['month_of_year'] = pd.to_datetime(monthly_revenue['month']).dt.month
monthly_revenue['year'] = pd.to_datetime(monthly_revenue['month']).dt.year
monthly_revenue['prev_month_revenue'] = monthly_revenue['total_price'].shift(1)
monthly_revenue['rolling_avg_3'] = monthly_revenue['total_price'].rolling(window=3).mean()
monthly_revenue['rolling_avg_6'] = monthly_revenue['total_price'].rolling(window=6).mean()

# Drop NaN
monthly_revenue = monthly_revenue.dropna()

print(f"\nFeature data shape: {monthly_revenue.shape}")
print(monthly_revenue.head())

# ============================================================
# FEATURES AND TARGET
# ============================================================
X = monthly_revenue[['month_num', 'month_of_year', 'year',
                      'prev_month_revenue', 'rolling_avg_3', 'rolling_avg_6']]
y = monthly_revenue['total_price']

# ============================================================
# TIME BASED SPLIT — NEVER random split for time series!
# ============================================================
split = int(len(monthly_revenue) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

# ============================================================
# LINEAR REGRESSION
# ============================================================
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_prediction = lr_model.predict(X_test)

print("\n=== LINEAR REGRESSION ===")
print(f"MAE: {mean_absolute_error(y_test, lr_prediction):,.0f}")
print(f"R2:  {r2_score(y_test, lr_prediction):.2f}")

# ============================================================
# RANDOM FOREST
# ============================================================
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_prediction = rf_model.predict(X_test)

print("\n=== RANDOM FOREST ===")
print(f"MAE: {mean_absolute_error(y_test, rf_prediction):,.0f}")
print(f"R2:  {r2_score(y_test, rf_prediction):.2f}")

# ============================================================
# PREDICT NEXT MONTH
# ============================================================
last_row = monthly_revenue.iloc[-1]
next_month_features = pd.DataFrame([{
    'month_num': last_row['month_num'] + 1,
    'month_of_year': (last_row['month_of_year'] % 12) + 1,
    'year': last_row['year'] + (1 if last_row['month_of_year'] == 12 else 0),
    'prev_month_revenue': last_row['total_price'],
    'rolling_avg_3': monthly_revenue['total_price'].tail(3).mean(),
    'rolling_avg_6': monthly_revenue['total_price'].tail(6).mean()
}])

lr_next = lr_model.predict(next_month_features)[0]
rf_next = rf_model.predict(next_month_features)[0]

print(f"\n=== NEXT MONTH PREDICTION ===")
print(f"Linear Regression: ${lr_next:,.0f}")
print(f"Random Forest:     ${rf_next:,.0f}")



plt.figure(figsize=(12, 6))
plt.plot(range(len(y_test)), y_test.values, label='Actual', marker='o')
plt.plot(range(len(y_test)), lr_prediction, label='Predicted', marker='x')
plt.title('Sales Forecast - Actual vs Predicted')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.legend()
plt.tight_layout()
plt.savefig('ml/sales_forecast.png')
plt.show()
print("Chart saved!")