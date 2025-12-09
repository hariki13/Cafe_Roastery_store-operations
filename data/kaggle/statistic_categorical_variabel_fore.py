import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load data
df = pd.read_csv('data/kaggle/fore.csv')
print("="*50)
print("CATEGORICAL VARIABLES STATISTICAL ANALYSIS")
print("="*50)

# get all categorical columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
print(f"\n📋 found {len(categorical_cols)} categorical columns: {categorical_cols}")
for col in categorical_cols:
    print(f"\n🔎 Analyzing Categorical Column: {col}")
    
    # 1. VALUE COUNTS
    value_counts = df[col].value_counts(dropna=False)
    print(f"\n📊 Value Counts for '{col}':")
    print(value_counts)

    # 2. UNIQUE VALUES
    unique_values = df[col].nunique(dropna=False)
    print(f"\n✨ Unique Values in '{col}': {unique_values}")

    # 3. MODE
    mode_value = df[col].mode()[0]
    mode_count = value_counts[mode_value]
    print(f"\n🏆 Mode of '{col}': '{mode_value}' (Count: {mode_count})")

    # 4. PLOTTING DISTRIBUTION
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=col, order=value_counts.index)
    plt.title(f"Distribution of '{col}'")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"data/kaggle/plots/{col}_distribution.png")
    plt.close()