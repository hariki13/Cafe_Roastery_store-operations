"""
Sample data generator for testing the Coffee Analytics module.
Creates realistic coffee shop sales data for demonstration.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=1000, start_date='2024-01-01', 
                         days=90, output_file='coffee sales dataset.csv'):
    """
    Generate sample coffee shop sales data.
    
    Parameters:
    - num_records: Number of transactions to generate
    - start_date: Start date for the data
    - days: Number of days to span
    - output_file: Output CSV filename
    """
    
    # Coffee products with base prices
    products = {
        'Espresso': 3.50,
        'Latte': 4.50,
        'Cappuccino': 4.25,
        'Americano': 3.75,
        'Mocha': 5.00,
        'Macchiato': 4.00,
        'Flat White': 4.50,
        'Cold Brew': 4.25,
        'Iced Latte': 4.75,
        'Caramel Frappuccino': 5.50,
        'Vanilla Latte': 5.00,
        'Hot Chocolate': 3.75,
        'Chai Latte': 4.50,
        'Matcha Latte': 5.25,
        'Drip Coffee': 2.50
    }
    
    # Product popularity weights (higher = more likely to be ordered)
    popularity = {
        'Espresso': 0.8,
        'Latte': 1.5,
        'Cappuccino': 1.2,
        'Americano': 1.0,
        'Mocha': 0.9,
        'Macchiato': 0.6,
        'Flat White': 0.7,
        'Cold Brew': 1.3,
        'Iced Latte': 1.4,
        'Caramel Frappuccino': 1.1,
        'Vanilla Latte': 1.0,
        'Hot Chocolate': 0.5,
        'Chai Latte': 0.8,
        'Matcha Latte': 0.7,
        'Drip Coffee': 1.6
    }
    
    # Payment methods
    payment_methods = ['card', 'cash']
    payment_weights = [0.7, 0.3]  # 70% card, 30% cash
    
    # Time distribution (simulating real coffee shop patterns)
    # Peak hours: 7-9 AM, 12-1 PM, 3-4 PM
    hour_weights = {
        0: 0.01, 1: 0.01, 2: 0.01, 3: 0.01, 4: 0.02, 5: 0.05,
        6: 0.08, 7: 0.15, 8: 0.18, 9: 0.12, 10: 0.08, 11: 0.07,
        12: 0.10, 13: 0.08, 14: 0.06, 15: 0.09, 16: 0.07, 17: 0.05,
        18: 0.04, 19: 0.03, 20: 0.02, 21: 0.01, 22: 0.01, 23: 0.01
    }
    
    # Day of week weights (weekend vs weekday patterns)
    day_weights = {
        0: 0.15,  # Monday
        1: 0.15,  # Tuesday
        2: 0.15,  # Wednesday
        3: 0.15,  # Thursday
        4: 0.18,  # Friday
        5: 0.12,  # Saturday
        6: 0.10   # Sunday
    }
    
    # Generate data
    np.random.seed(42)
    random.seed(42)
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    records = []
    product_names = list(products.keys())
    product_weights = [popularity[p] for p in product_names]
    
    for _ in range(num_records):
        # Generate random day within range
        day_offset = random.choices(range(days), 
                                    weights=[day_weights[d % 7] for d in range(days)])[0]
        
        # Generate random hour
        hour = random.choices(list(hour_weights.keys()), 
                             weights=list(hour_weights.values()))[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        transaction_time = start + timedelta(days=day_offset, hours=hour, 
                                             minutes=minute, seconds=second)
        
        # Select product
        coffee_name = random.choices(product_names, weights=product_weights)[0]
        base_price = products[coffee_name]
        
        # Add some price variation (+/- 15%)
        price = round(base_price * random.uniform(0.85, 1.15), 2)
        
        # Select payment method
        payment = random.choices(payment_methods, weights=payment_weights)[0]
        
        records.append({
            'datetime': transaction_time.strftime('%Y-%m-%d %H:%M:%S'),
            'coffee_name': coffee_name,
            'money': price,
            'cash_type': payment
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(records)
    df = df.sort_values('datetime').reset_index(drop=True)
    df.to_csv(output_file, index=False)
    
    print(f"Generated {num_records} sample records")
    print(f"Date range: {start_date} to {(start + timedelta(days=days)).strftime('%Y-%m-%d')}")
    print(f"Saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    # Generate sample dataset for testing
    df = generate_sample_data(num_records=1000, days=90)
    print("\nSample data preview:")
    print(df.head(10))
    print(f"\nProducts: {df['coffee_name'].nunique()}")
    print(f"Total sales: ${df['money'].sum():.2f}")
