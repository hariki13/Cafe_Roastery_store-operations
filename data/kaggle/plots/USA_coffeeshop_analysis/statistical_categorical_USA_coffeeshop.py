import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# set visualization style (makes plots prettier)
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# load data
df = pd.read_csv('data/kaggle/USA_Coffeeshop.csv')
print("="*50)
print("CATEGORICAL VARIABLES STATISTICAL ANALYSIS - USA Coffeeshop Dataset")
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
    total_values = len(df[col])
    missing_count = df[col].isnull().sum()
    print(f"Total Values in '{col}': {total_values}")
    print(f"Missing Values in '{col}': {missing_count}")
    print(f"\n✨ Unique Values in '{col}': {unique_values}")

    # 3. MODE
    mode_value = df[col].mode()[0]
    mode_count = value_counts[mode_value]
    print(f"\n🏆 Mode of '{col}': '{mode_value}' (Count: {mode_count})")

    # calculate percentage of distribution for mode
    mode_percentage = (mode_count / total_values) * 100
    print(f"Mode Percentage of Total: {mode_percentage:.2f}%")
    pct_distribution = (value_counts / total_values * 100).round(2)
    print(f"\n📈 Percentage Distribution for '{col}':")
    print(pct_distribution)

    # checking for dominance
    if mode_percentage > 50:
        print(f"⚠️ The mode '{mode_value}' dominates the column '{col}' with {mode_percentage:.2f}% of total values.")
    else:
        print(f"✅ No single category dominates the column '{col}' (mode percentage ≤ 50%).")
    top_categories = pct_distribution.head(3)

    if len(top_categories) > 1:
        combined_percentage = top_categories.sum()
        if combined_percentage > 70:
            print(f"⚠️ The top {len(top_categories)} categories together account for {combined_percentage:.2f}% of total values in '{col}'.")
        else:
            print(f"✅ The top {len(top_categories)} categories do not dominate the column '{col}' (combined percentage ≤ 70%).")
    elif unique_values < 5:
        print(f"⚠️ Only {unique_values} unique categories found in '{col}'. Consider reviewing this column for data quality.")

    #  checking for low frequency categories
    low_freq_threshold = 0.05  # 5%
    low_freq_categories = pct_distribution[pct_distribution < low_freq_threshold]
    if not low_freq_categories.empty:
        print(f"⚠️ Low frequency categories in '{col}' (less than {low_freq_threshold*100}% of total):")
        print(low_freq_categories)
    else:
        print(f"✅ No low frequency categories found in '{col}' (all categories ≥ {low_freq_threshold*100}%).")

    # check for rare categories (less than 1% of total)
    rare_threshold = 1.0  # 1%
    rare_categories = pct_distribution[pct_distribution < rare_threshold]
    if not rare_categories.empty:
        print(f"⚠️ Rare categories in '{col}' (less than {rare_threshold}% of total):")
        print(rare_categories)
    else:
        print(f"✅ No rare categories found in '{col}' (all categories ≥ {rare_threshold}%).")

    

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

# pie chart for column 'Product' and 'Product Type' distribution
for pie_col in ['Product', 'Product Type']:
    if pie_col in df.columns:
        value_counts = df[pie_col].value_counts(dropna=False)
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Value Distribution of '{pie_col}'")
        plt.tight_layout()
        # Use safe filename (replace space with underscore)
        safe_filename = pie_col.replace(' ', '_')
        plt.savefig(f"data/kaggle/plots/{safe_filename}_piechart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: data/kaggle/plots/{safe_filename}_piechart.png")
