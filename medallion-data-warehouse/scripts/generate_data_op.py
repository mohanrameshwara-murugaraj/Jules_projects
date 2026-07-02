import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_orders_and_payments(num_orders=1000000):
    print(f"Generating {num_orders} orders and payments...")

    # Read existing customers and products to reference
    try:
        customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
        products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
        customer_ids = customers['customer_id'].dropna().tolist()
        product_ids = products['product_id'].dropna().tolist()
    except FileNotFoundError:
        print("Run generate_data_cp.py first to create customers and products.")
        customer_ids = [f"CUST-{100000+i}" for i in range(100000)]
        product_ids = [f"PROD-{10000+i}" for i in range(10000)]

    orders_data = []
    payments_data = []

    statuses = ['pending', 'shipped', 'delivered', 'cancelled', 'PENDING', 'Delivered ']
    payment_methods = ['credit_card', 'paypal', 'apple_pay', 'bank_transfer', 'Credit Card']
    payment_statuses = ['success', 'failed', 'refunded', 'SUCCESS']

    start_date = datetime.now() - timedelta(days=365*2)

    for i in range(num_orders):
        order_id = f"ORD-{1000000 + i}"

        # Simulating orphaned orders (no valid customer)
        cust_id = random.choice(customer_ids) if random.random() > 0.05 else f"CUST-UNKNOWN-{random.randint(1,100)}"
        prod_id = random.choice(product_ids)

        # Generate order date
        order_date = fake.date_time_between(start_date=start_date, end_date='now')

        # Simulating future dates or bad formats
        if random.random() < 0.01:
            order_date = datetime.now() + timedelta(days=random.randint(1, 30))

        order_date_str = order_date.isoformat() if random.random() > 0.02 else order_date.strftime("%d-%m-%Y")

        quantity = random.randint(1, 10)
        # 1% chance of negative quantity
        if random.random() < 0.01:
            quantity = -quantity

        status = random.choice(statuses)

        orders_data.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "product_id": prod_id,
            "order_date": order_date_str,
            "quantity": quantity,
            "status": status
        })

        # Generate payment for the order
        if random.random() > 0.05: # 5% orders have no payment record
            payment_id = f"PAY-{1000000 + i}"
            payment_date = order_date + timedelta(hours=random.randint(0, 48))

            payments_data.append({
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_method": random.choice(payment_methods),
                "amount": round(random.uniform(10.0, 1000.0), 2),
                "status": random.choice(payment_statuses),
                "payment_date": payment_date.isoformat()
            })

            # Simulate duplicate payments
            if random.random() < 0.02:
                payments_data.append(payments_data[-1].copy())

    orders_df = pd.DataFrame(orders_data)
    payments_df = pd.DataFrame(payments_data)

    orders_df.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
    payments_df.to_csv(os.path.join(DATA_DIR, "payments.csv"), index=False)
    print(f"Saved orders and payments to {DATA_DIR}")

if __name__ == "__main__":
    # Reduce size for local quick generation during portfolio building
    generate_orders_and_payments(1000000)
