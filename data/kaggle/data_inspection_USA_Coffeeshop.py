import pandas as pd
import numpy as np


# ====lOAD AND INSPECT DATA===
print("\n📂 Loading data...")
df = pd.read_csv('data/kaggle/USA_Coffeeshop.csv')
print("✅ Data loaded successfully.")

# ====INITIAL DATA INSPECTION===
print("="*50)
print("INITIAL DATA INSPECTION")
print("="*50)
# basic review of the data
print(f"\n🖼️ shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"💾 memory: {df.memory_usage(deep=True).sum()/ 1024**2:.2f} MB")

# 1. FIRST LOOK - Top rows
print("\n📌First 5 rows:")
print(df.head())

# 2. LAST LOOK - Bottom rows (catch data loading issues)
print("\n📌Last 5 rows:")
print(df.tail())