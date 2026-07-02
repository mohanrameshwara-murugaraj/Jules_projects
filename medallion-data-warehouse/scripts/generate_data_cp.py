import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
# Fix seed for reproducibility in a portfolio
Faker.seed(42)
np.random.seed(42)
random.seed(42)

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_customers(num_records=100000):
    print(f"Generating {num_records} customers...")
    data = []
    for i in range(num_records):
        # Introducing invalid customer IDs and nulls
        customer_id = f"CUST-{100000 + i}" if random.random() > 0.01 else f"INVALID-{random.randint(100,999)}"
        customer_id = None if random.random() > 0.995 else customer_id

        email = fake.email() if random.random() > 0.02 else None

        data.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "phone": fake.phone_number() if random.random() > 0.1 else None,
            "address": fake.street_address().replace('\n', ', '),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "country": "USA" if random.random() > 0.05 else fake.country(),
            "registration_date": fake.date_between(start_date='-5y', end_date='today').isoformat(),
            "is_active": random.choice([True, False, None, 'yes', 'no']) # Inconsistencies
        })

    df = pd.DataFrame(data)
    # Add some duplicates
    duplicates = df.sample(frac=0.01)
    df = pd.concat([df, duplicates])

    output_path = os.path.join(DATA_DIR, "customers.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved customers to {output_path}")
    return df

def generate_products(num_records=10000):
    print(f"Generating {num_records} products...")
    data = []
    categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Sports', 'Books', 'Beauty']

    for i in range(num_records):
        product_id = f"PROD-{10000 + i}"
        # Bad product IDs
        if random.random() < 0.02:
            product_id = f"BAD-PROD-{random.randint(1,999)}"

        category = random.choice(categories)

        # Simulating data issues like negative price
        base_price = round(random.uniform(5.0, 500.0), 2)
        price = base_price if random.random() > 0.005 else -base_price

        data.append({
            "product_id": product_id,
            "product_name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
            "category": category if random.random() > 0.01 else None,
            "brand": fake.company(),
            "price": price,
            "cost": round(price * random.uniform(0.3, 0.7), 2) if price > 0 else 0,
            "currency": random.choice(["USD", "USD", "USD", "EUR", "GBP", "cad"]) # Inconsistencies
        })

    df = pd.DataFrame(data)
    output_path = os.path.join(DATA_DIR, "products.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved products to {output_path}")
    return df

if __name__ == "__main__":
    generate_customers(100000)
    generate_products(10000)
