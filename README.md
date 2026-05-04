# E-Commerce Data Pipeline

## Overview
An industry-level E-Commerce Data Pipeline project built from scratch showing complete Data Engineering and Data Science workflow — from data generation to ML-powered interactive dashboard.

---

## Project Evolution
| Phase | Technology | Description |
|-------|-----------|-------------|
| 1 | Python + MySQL | Data generation and database setup |
| 2 | Pandas + Airflow | ETL pipeline with automated scheduling |
| 3 | Streamlit + Plotly | Interactive analytics dashboard |
| 4 | Scikit-learn | Machine Learning models |

---

## Tech Stack
- **Language:** Python 3
- **Database:** MySQL
- **Data Processing:** Pandas, SQLAlchemy
- **Workflow Orchestration:** Apache Airflow
- **Dashboard:** Streamlit, Plotly
- **Machine Learning:** Scikit-learn
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git

---

## Project Structure
```
ecommerce-data-pipeline/
├── data/                          
│   ├── customer.csv
│   ├── product.csv
│   ├── order.csv
│   └── order_items.csv
├── dags/                          
│   └── ecommerce_etl_dag.py       
├── dashboard/                     
│   └── app.py                     
├── ml/                            
│   ├── sales_forecast.py          
│   ├── churn_prediction.py        
│   └── customer_segmentation.py   
├── docker/                        
├── generate_data.py               
├── load_to_MYSQL.py               
├── etl_pipeline.py                
├── requirements.txt               
├── .env                           
└── .gitignore                     
```

---

## Dataset
Synthetically generated realistic e-commerce dataset:

| Table | Records | Description |
|-------|---------|-------------|
| customers | 10,000 | Customer demographics and behavior |
| products | 1,000 | Product catalog with pricing |
| orders | 50,000 | Order transactions with trend |
| order_items | 45,000 | Individual order line items |

**Key Features:**
- 5 years of historical data (2021-2026)
- Growth trend built into sales data
- Holiday seasonality (30% boost in Nov, Dec, Jan)
- Realistic customer demographics

---

## ETL Pipeline

### Pipeline Architecture
```
MySQL Database
     ↓ Extract
Pandas DataFrames
     ↓ Transform
Merged & Analyzed Data
     ↓ Load
Reporting Tables (MySQL)
     ↓ Automate
Apache Airflow (Daily Schedule)
```

### Airflow DAG Tasks
```
extract_data → transform_data → load_data → summary_data
```

### Business Insights Generated
- Revenue by category
- Top 10 customers by spending
- Monthly sales trend
- Revenue by payment method
- Revenue by device type
- Revenue by traffic source
- Order status breakdown

---

## Streamlit Dashboard

### Features
- Interactive Plotly charts
- Sidebar filters (Category, Payment, Device, Status, Date Range)
- Monthly sales trend line chart
- Payment method pie chart
- Top 10 customers table
- Customer search functionality
- Download report button
- ML insights tab

### Running the Dashboard
```bash
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

## Live Dashboard
Access the live dashboard at: http://35.172.117.131:8501

---

## Machine Learning Models

### Model 1 — Sales Forecasting
- **Algorithm:** Linear Regression + Random Forest
- **Features:** Month number, seasonality, rolling averages, previous month revenue
- **Result:** R2 Score: 0.65 (Linear Regression)
- **Output:** Next month revenue prediction

### Model 2 — Customer Churn Prediction
- **Algorithm:** Logistic Regression + Random Forest Classifier
- **Features:** Total orders, total spent, avg order value, age, device type, traffic source
- **Result:** 63% accuracy
- **Output:** Churn probability per customer

**Top Features for Churn:**
1. Total Spent (0.29)
2. Avg Order Value (0.26)
3. Age (0.23)
4. Total Orders (0.08)

### Model 3 — Customer Segmentation
- **Algorithm:** K-Means Clustering (K=4)
- **Method:** RFM Analysis (Recency, Frequency, Monetary)
- **Segments:**

| Segment | Customers | Avg Orders | Avg Spent | Days Inactive |
|---------|-----------|------------|-----------|---------------|
| VIP | 1,726 (17.4%) | 8.4 | $45,146 | 191 |
| Regular | 3,715 (37.4%) | 5.7 | $28,581 | 246 |
| At-Risk | 3,035 (30.6%) | 3.3 | $14,920 | 263 |
| Dormant | 1,458 (14.7%) | 2.8 | $13,698 | 988 |

---

## How to Run

### Prerequisites
- Python 3.8+
- MySQL Server
- Docker Desktop (for Airflow)

### Step 1 — Setup Environment
```bash
# Clone the repo
git clone https://github.com/jd878-gif/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2 — Configure Environment
Create `.env` file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=ecommerce_db
```

### Step 3 — Generate and Load Data
```bash
# Generate synthetic data
python generate_data.py

# Load to MySQL
python load_to_MYSQL.py
```

### Step 4 — Run ETL Pipeline
```bash
python etl_pipeline.py
```

### Step 5 — Run Airflow
```bash
cd airflow
docker compose up -d
```
Access Airflow UI at: `http://localhost:8080`
- Username: `airflow`
- Password: `airflow`

### Step 6 — Run Dashboard
```bash
streamlit run dashboard/app.py
```

### Step 7 — Run ML Models
```bash
python ml/sales_forecast.py
python ml/churn_prediction.py
python ml/customer_segmentation.py
```



## API Endpoints (ETL Reporting Tables)
| Table | Description |
|-------|-------------|
| report_revenue_by_category | Revenue grouped by product category |
| report_customer_spending | Total spending per customer |
| report_top_ten_customers | Top 10 highest spending customers |
| report_monthly_sale | Monthly revenue trend |
| report_payment_revenue | Revenue by payment method |
| device_revenue | Revenue by device type |
| traffic_revenue | Revenue by traffic source |
| order_stauts | Order status breakdown |

---

## Author
**Jeet Dave**
[GitHub](https://github.com/jd878-gif/)