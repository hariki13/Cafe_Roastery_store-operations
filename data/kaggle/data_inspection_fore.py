import pandas as pd
import numpy as np

# load your data
df = pd.read_csv('data/kaggle/fore.csv')

print("="*50)
print("INITIAL DATA INSPECTION")
print("="*50)

# 1. FIRST LOOK - Top rows
print("\n📌First 5 rows:")
print(df.head())