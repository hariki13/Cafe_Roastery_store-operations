import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Use non-interactive backend for headless environment
plt.switch_backend('Agg')

# Create output directory for plots
os.makedirs('data/kaggle/plots', exist_ok=True)

# load your data
df = pd.read_csv('data/kaggle/fore.csv')
print("="*50)
print("STATISTICAL DATA INSPECTION")
print("="*50)

# BASIC STATISTIC- THE FOUNDATION FOR DATA UNDERSTANDING:

print("="*50)
print("NUMERICAL VARIABLES STATISTICAL ANALYSIS")
print("="*50)

# get all numerical columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(f"\n📋 found {len(numerical_cols)} numerical columns: {numerical_cols}")

# 1. STATISTICAL SUMMARY (GIVING 80% INSIGHTS INTO DATA DISTRIBUTION)
print("\n📊 Statistical Summary for Numerical Columns:")
print(df[numerical_cols].describe())

# explanation of describe() output
# print("\n🔍 Explanation of Statistical Summary:")
#          price
# count    500. 00    ← How many values (non-null)
# mean      45.50    ← Average price
# std       12.30    ← Standard deviation (spread)
# min       10.00    ← Minimum price
# 25%       38.00    ← 25% of prices are below this (Q1)
# 50%       45.00    ← Median (middle value) (Q2)
# 75%       52.00    ← 75% of prices are below this (Q3)
# max      120.00    ← Maximum price

# FOE EACH NUMERICAL COLUMN, ASK:
for col in numerical_cols:
    print(f"\n🔎 Analyzing Numerical Column: {col}")
    
    mean_val = df[col].mean()
    median_val = df[col].median()
    std_val = df[col].std()
    min_val = df[col].min()
    max_val = df[col].max()
    print(f" Mean: {mean_val:.2f}, Median: {median_val:.2f}, Std: {std_val:.2f}, Min: {min_val:.2f}, Max: {max_val:.2f}")

    # 🔍 KEY INSIGHTS:

# 1. is data skewed?
for col in numerical_cols:
    skewness = df[col].skew()
    if skewness > 1:
        skew_type = "highly right-skewed"
    elif skewness < -1:
        skew_type = "highly left-skewed"
    elif 0.5 < skewness <= 1:
        skew_type = "moderately right-skewed"
    elif -1 <= skewness < -0.5:
        skew_type = "moderately left-skewed"
    else:
        skew_type = "approximately symmetric"
    print(f"\n🔎 Skewness of {col}: {skewness:.2f} ({skew_type})")

    
# visualize skewness with histogram
    plt.figure(figsize=(10, 4))
    sns.histplot(df[col].dropna(), kde=True, bins=30)
    plt.title(f'Distribution of {col} (Skewness: {skewness:.2f})')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.savefig(f'data/kaggle/plots/skewness_{col}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: plots/skewness_{col}.png")


    # 2. is there high variability?
    coef_var = (std_val / mean_val) * 100 if mean_val != 0 else 0 #coefficient of variation
    if coef_var > 50:
        variability = "high variability"
    elif 20 < coef_var <= 50:
        variability = "moderate variability"
    else:
        variability = "low variability"
    print(f"\n🔎 Coefficient of Variation for {col}: {coef_var:.1f}% ({variability})")

    # 3. are there outliers?
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_count = outliers.shape[0]
    print(f"\n🔎 Outlier Detection for {col}: Found {outlier_count} outliers")
    
    if len(outliers) > 0:
        print(f" . outlier values: {sorted(outliers[col].values)[:10]}")

    # 2. DISTRIBUTION ANALYSIS
    plt.figure(figsize=(10, 4))
    sns.histplot(df[col].dropna(), kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.savefig(f'data/kaggle/plots/distribution_{col}.png', dpi=150, bbox_inches='tight')
    plt.close()
    # print(f"   ✅ Saved: plots/distribution_{col}.png")
    
    # 3. OUTLIER DETECTION USING BOXPLOT
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot of {col}')
    plt.xlabel(col)
    plt.savefig(f'data/kaggle/plots/boxplot_{col}.png', dpi=150, bbox_inches='tight')
    plt.close()
    # print(f"   ✅ Saved: plots/boxplot_{col}.png")
    
# 4. CORRELATION WITH OTHER NUMERICAL VARIABLES (once, outside loop)
corr_matrix = df[numerical_cols].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix of Numerical Variables')
plt.savefig('data/kaggle/plots/correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
# print("\n✅ Saved: plots/correlation_matrix.png")

# 5. vertical box plot for all numerical variables
plt.figure(figsize=(12, 6))
df_melted = df[numerical_cols].melt(var_name='Variable', value_name='Value')
sns.boxplot(x='Variable', y='Value', data=df_melted)
plt.title('Boxplot of All Numerical Variables')
plt.xticks(rotation=45)
plt.savefig('data/kaggle/plots/boxplot_all_numerical.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Saved: plots/boxplot_all_numerical.png")

# 6. seaborn version (prettier)
plt.figure(figsize=(12, 6))
sns.boxenplot(data=df[numerical_cols], palette='Set3')
plt.title('Boxenplot of All Numerical Variables')
ax.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.savefig('data/kaggle/plots/boxenplot_all_numerical.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Saved: plots/boxenplot_all_numerical.png")