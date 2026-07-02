import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_returns_and_marketing():
    print(f"Generating returns and marketing...")

    try:
        orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
        order_ids = orders['order_id'].dropna().tolist()
    except FileNotFoundError:
        print("Run previous generators first.")
        order_ids = [f"ORD-{1000000+i}" for i in range(1000000)]

    # RETURNS
    returns_data = []
    reasons = ['defective', 'wrong_item', 'not_needed', 'other', 'Defective ']

    for i, order_id in enumerate(order_ids):
        # 5% of orders are returned
        if random.random() < 0.05:
            returns_data.append({
                "return_id": f"RET-{100000 + i}",
                "order_id": order_id,
                "return_date": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
                "reason": random.choice(reasons),
                "refund_amount": round(random.uniform(5.0, 500.0), 2)
            })

    pd.DataFrame(returns_data).to_csv(os.path.join(DATA_DIR, "returns.csv"), index=False)

    # MARKETING
    marketing_data = []
    channels = ['Email', 'Social Media', 'Search', 'Affiliate', 'social media']

    for i in range(5000): # 5k campaigns
        marketing_data.append({
            "campaign_id": f"CAMP-{1000 + i}",
            "campaign_name": f"{fake.word().capitalize()} {fake.word().capitalize()} Promo",
            "channel": random.choice(channels),
            "start_date": fake.date_between(start_date='-2y', end_date='now').isoformat(),
            "end_date": fake.date_between(start_date='-1y', end_date='+1y').isoformat(),
            "budget": round(random.uniform(100.0, 50000.0), 2)
        })

    pd.DataFrame(marketing_data).to_csv(os.path.join(DATA_DIR, "marketing.csv"), index=False)
    print(f"Saved returns and marketing to {DATA_DIR}")

if __name__ == "__main__":
    generate_returns_and_marketing()
