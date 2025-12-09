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
    plt.figure(figsize=(12, 6))
    
    # Use horizontal bar chart if more than 10 categories or long text
    if unique_values > 10 or df[col].astype(str).str.len().max() > 20:
        # Show only top 20 categories for readability
        top_categories = value_counts.head(20)
        plt.barh(range(len(top_categories)), top_categories.values)
        plt.yticks(range(len(top_categories)), top_categories.index, fontsize=9)
        plt.xlabel('Count')
        plt.title(f"Distribution of '{col}' (Top 20 Categories)" if unique_values > 20 else f"Distribution of '{col}'")
        plt.gca().invert_yaxis()  # Highest count at top
    else:
        # Vertical bar chart for fewer categories
        sns.countplot(data=df, x=col, order=value_counts.index)
        plt.title(f"Distribution of '{col}'")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.xlabel(col)
        plt.ylabel('Count')
    
    plt.tight_layout()
    plt.savefig(f"data/kaggle/plots/{col}_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: data/kaggle/plots/{col}_distribution.png")