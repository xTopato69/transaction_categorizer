import csv
import random
from datetime import datetime, timedelta
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.paths import get_raw_data_path, ensure_dir_exists

categories = [
    "Food & Dining", "Utilities", "Shopping", "Entertainment",
    "Travel", "Health", "Education"
]
merchants = [
    "KFC", "Starbucks", "Amazon", "Netflix", "Uber", "Pharmacy", "Coursera", "Electricity Board", "Water Supply"
]
descriptions = [
    "Lunch at", "Coffee at", "Order from", "Subscription to", "Ride with", "Medicine from", "Course on", "Bill payment to"
]
payment_methods = ["Credit Card", "Debit Card", "Wallet", "Net Banking"]
user_ids = [f"user_{i}" for i in range(1, 6)]

def random_date():
    start = datetime.now() - timedelta(days=180)
    return (start + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d %H:%M:%S")

def generate_sample_data():
    output_path = get_raw_data_path()
    ensure_dir_exists(output_path)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'transaction_id', 'amount', 'description', 'merchant',
            'date', 'category', 'user_id', 'payment_method'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, 101):
            cat = random.choice(categories)
            merchant = random.choice(merchants)
            desc = f"{random.choice(descriptions)} {merchant}"
            row = {
                "transaction_id": f"txn_{i:04d}",
                "amount": round(random.uniform(10, 5000), 2),
                "description": desc,
                "merchant": merchant,
                "date": random_date(),
                "category": cat,
                "user_id": random.choice(user_ids),
                "payment_method": random.choice(payment_methods)
            }
            writer.writerow(row)
    
    print(f"Sample transaction data generated at {output_path}")

if __name__ == "__main__":
    generate_sample_data()
