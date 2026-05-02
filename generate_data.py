from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

customer = []
for i in range(10000):
    customer.append({
        'customer_id' : f"CUST{i+1:04d}",
        'name': fake.name(),
        'email' : fake.email(),
        'city' : fake.city(),
        'age' : random.randint(16,80),
        'gender' : random.choice(['Male', 'Female']),
        'phone_number' : fake.phone_number(),
        'sign_up_date' : fake.date_between(start_date='-2y', end_date='today'),
        'device_type' : random.choice(['mobile', 'desktop', 'tablet']),
        'traffic_source' : random.choice(['organic', 'paid', 'social', 'email', 'referral'])

    })

customer_df = pd.DataFrame(customer)
customer_df.to_csv('data/customer.csv', index=False)
print(f"Generated {len(customer_df)} customers!")

product = []
for i in range(1000):
    price = round(random.uniform(10,5000),2)
    product.append({
        'product_id' : f"PROD{i+1:04d}",
        'name': random.choice(['Wireless Headphones', 'Running Shoes', 'Coffee Maker', 'Smartphones', 'Laptop', 'Smart TV', 'T-shirts', 'Jeans', 'Hoodies', 'Sneakers', 'Robotic Vaccums', 'Blender set', 'Shampoo', 'Lipstcik', 'Protien Powder', 'Ficton Novel', 'Board Games']),
        'discount' : round(random.uniform(0.03,0.6),2),
        'price': price,
        'category' : random.choice(['Cleaning Supplies', 'Electronics', 'Home Decor', 'Furniture','Mens wear', 'womens wear', 'kids', 'summer essentials','Holiday gift guide', 'Artisanal Foods']),
        'supplier' : random.choice(['GlobalTech', 'FastShip', 'PrimeSeller', 'MegaSupply', 'QuickStock']),
        'rating' : random.randint(1,5),
        'cost_price' : round(random.uniform(5, price*0.7),2),
        'stock' : random.randint(0,500)

    })
product_df = pd.DataFrame(product)
product_df.to_csv('data/product.csv', index=False)
print(f"Generated {len(product_df)} products!")

order = []
for i in range(50000):
    order_date = fake.date_between(start_date='-5y', end_date='today')
    start_date = datetime(2021, 1, 1).date()
    days_diff = (order_date - start_date).days
    base_amount = random.uniform(20, 5000)
    trend = 1 + (days_diff / 1825) * 0.5
    seasonality = 1 + 0.3 * (order_date.month in [11, 12, 1])
    amount = round(base_amount * trend * seasonality, 2)
    order.append({
        'order_id' : f"ORD{i+1:04d}",
        'customer_id': f"CUST{random.randint(1,10000):04d}",
        'order_date': order_date,
        'order_status' : random.choice(['Pending', 'Shipped', 'Delivered', 'Returned','Cancelled']),
        'amount': round(random.uniform(20, 10000), 2),
        'payment_method' : random.choice(['Card', 'UPI', 'Cash', 'Wallet']),
        'shipping_cost' : round(random.uniform(10,100),2),
        'delivery_date' : order_date + timedelta(days=random.randint(2,10)),
        'is_returned' : random.choice(['True', 'False'])

    })
order_df = pd.DataFrame(order)
order_df.to_csv('data/order.csv', index=False)
print(f"Generated {len(order_df)} orders!")

order_items = []
for i in range(45000):
    unit_price = round(random.uniform(10, 5000), 2)
    days_diff = random.randint(0, 1825)  
    trend = 1 + (days_diff / 1825) * 0.5
    seasonality = 1 + 0.3 * random.choice([0, 0, 0, 1])
    quantity = random.randint(1, 5)
    discount_applied = round(random.uniform(0, 0.6), 2)
    total_price = round(unit_price * quantity * (1 - discount_applied), 2)
    order_items.append({
        'order_id' : f"ORD{random.randint(1,50000):04d}",
        'product_id' : f"PROD{random.randint(1,1000):04d}",
        'unit_price' : unit_price,
        'quantity' : quantity,
        'total_price' : total_price,
        'discount_applied' : discount_applied

    })

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv('data/order_items.csv', index=False)
print(f"Generated {len(order_items_df)} order_items!")