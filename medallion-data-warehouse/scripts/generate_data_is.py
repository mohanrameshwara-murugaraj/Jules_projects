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

def generate_inventory_and_shipments():
    print(f"Generating inventory and shipments...")

    try:
        products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
        orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
        product_ids = products['product_id'].dropna().tolist()
        order_ids = orders['order_id'].dropna().tolist()
    except FileNotFoundError:
        print("Run previous generators first.")
        product_ids = [f"PROD-{10000+i}" for i in range(10000)]
        order_ids = [f"ORD-{1000000+i}" for i in range(1000000)]

    # INVENTORY
    inventory_data = []
    warehouses = ['WH-EAST', 'WH-WEST', 'WH-CENTRAL', 'WH-SOUTH', 'WH-NORTH', 'unknown']

    for i in range(len(product_ids) * 3): # 3 records per product approx
        prod_id = random.choice(product_ids)
        warehouse = random.choice(warehouses)

        inventory_data.append({
            "inventory_id": f"INV-{100000 + i}",
            "product_id": prod_id,
            "warehouse_id": warehouse,
            "quantity_on_hand": random.randint(-10, 1000), # Allow negative for data issues
            "last_updated": fake.date_time_between(start_date='-1y', end_date='now').isoformat()
        })

    pd.DataFrame(inventory_data).to_csv(os.path.join(DATA_DIR, "inventory.csv"), index=False)

    # SHIPMENTS
    shipments_data = []
    carriers = ['FedEx', 'UPS', 'USPS', 'DHL', 'fedex', 'Ups']

    for i, order_id in enumerate(order_ids):
        # 80% of orders have shipments
        if random.random() < 0.8:
            ship_date = fake.date_time_between(start_date='-2y', end_date='now')
            estimated_delivery = ship_date + timedelta(days=random.randint(1, 7))
            actual_delivery = estimated_delivery + timedelta(days=random.randint(-2, 5)) if random.random() > 0.2 else None

            # Bad dates simulation
            if random.random() < 0.01 and actual_delivery:
                actual_delivery = ship_date - timedelta(days=1) # Delivered before shipped

            shipments_data.append({
                "shipment_id": f"SHP-{100000 + i}",
                "order_id": order_id,
                "carrier": random.choice(carriers),
                "tracking_number": fake.bothify(text='1Z################'),
                "shipment_date": ship_date.isoformat(),
                "estimated_delivery_date": estimated_delivery.isoformat(),
                "actual_delivery_date": actual_delivery.isoformat() if actual_delivery else None,
                "status": random.choice(['in_transit', 'delivered', 'exception', 'returned'])
            })

    pd.DataFrame(shipments_data).to_csv(os.path.join(DATA_DIR, "shipments.csv"), index=False)
    print(f"Saved inventory and shipments to {DATA_DIR}")

if __name__ == "__main__":
    generate_inventory_and_shipments()
