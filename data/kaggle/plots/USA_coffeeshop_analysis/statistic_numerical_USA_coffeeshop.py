import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# load datadf 
df = pd.read_csv('data/kaggle/USA_Coffeeshop.csv')
print("="*50)
print("NUMERICAL VARIABLES STATISTICAL ANALYSIS")
print("="*50)

# set visualization style (makes plots prettier)
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# get all numerical columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(f"\n📋 found {len(numerical_cols)} numerical columns: {numerical_cols}")
for col in numerical_cols:
    print(f"\n🔎 Analyzing Numerical Column: {col}")
    
    # 1. DESCRIPTIVE STATISTICS
    desc_stats = df[col].describe()
    print(f"\n📊 Descriptive Statistics for '{col}':")
    print(desc_stats)

    for col in numerical_cols:
        print(f"\n🔎 Analyzing Numerical Column: {col}")

        mean_val = df[col].mean()
        median_val = df[col].median()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        print(f"\n📊 Descriptive Statistics for '{col}':")
        print(f"Mean: {mean_val}")
        print(f"Median: {median_val}")
        print(f"Standard Deviation: {std_val}")
        print(f"Minimum: {min_val}")
        print(f"Maximum: {max_val}")

    # 2. data skewed
    if mean_val > median_val*1.1: #*1.1 to allow some tolerance is mean noticeably skewed larger than median 
        print(f"⚠️ The data in '{col}' is right-skewed (mean > median). Consider transformation.")
    elif mean_val < median_val*0.9:
        print(f"⚠️ The data in '{col}' is left-skewed (mean < median). Consider transformation.")
    else:
        print(f"✅ The data in '{col}' is approximately symmetric (mean ≈ median).")
    
    # 3. high variability
    if std_val > mean_val*0.5:
        print(f"⚠️ The data in '{col}' has high variability (std dev > 50% of mean).")
    else:
        print(f"✅ The data in '{col}' has acceptable variability (std dev ≤ 50% of mean).")

    # 4. outliers detection
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_count = outliers.shape[0]
    if outlier_count > 0:
        print(f"⚠️ Found {outlier_count} outliers in '{col}' using IQR method.")
    else:
        print(f"✅ No outliers detected in '{col}' using IQR method.")
    

    # 3. PLOTTING DISTRIBUTION
    plt.figure(figsize=(10, 6))
    
    # Histogram
    sns.histplot(df[col].dropna(), bins=30, kde=True, color='skyblue')
    plt.title(f"Distribution of '{col}'")
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f"data/kaggle/plots/{col}_histogram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: data/kaggle/plots/{col}_histogram.png")
    
    # Boxplot
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df[col], color='lightgreen')
    plt.title(f"Boxplot of '{col}'")
    plt.xlabel(col)
    plt.tight_layout()
    plt.savefig(f"data/kaggle/plots/{col}_boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: data/kaggle/plots/{col}_boxplot.png")

    # pie chart for value distribution (only if unique values are less than 10)
    unique_values = df[col].nunique()
    if unique_values <= 10:
        value_counts = df[col].value_counts(dropna=False)
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Value Distribution of '{col}'")
        plt.tight_layout()
        plt.savefig(f"data/kaggle/plots/{col}_piechart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: data/kaggle/plots/{col}_piechart.png")
    else:
        print(f"ℹ️ Skipping pie chart for '{col}' due to high unique value count ({unique_values}).")
    
    # density plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(df[col].dropna(), fill=True, color='orange')
    plt.title(f"Density Plot of '{col}'")
    plt.xlabel(col)
    plt.ylabel('Density')
    plt.tight_layout()
    plt.savefig(f"data/kaggle/plots/{col}_densityplot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: data/kaggle/plots/{col}_densityplot.png")