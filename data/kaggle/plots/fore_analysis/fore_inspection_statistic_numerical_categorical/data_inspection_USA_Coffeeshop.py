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

# 3. column information
print("\n"+"="*60)
print("DATA STRUCTURE")
print("="*60)
print(f"\n📋columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:>2}. {col:30s} | dtype: {str(df[col].dtype)})")

# 4.type breakdown
numerical = df.select_dtypes(include=[np.number]).columns.tolist()
categorical = df.select_dtypes(include=['object', 'category']).columns.tolist()
datetime = df.select_dtypes(include=['datetime64']).columns.tolist()
print(f"\n🔢 Numerical columns: {len(numerical)}")
print(f"🗂️ Categorical columns: {len(categorical)}")
print(f"📅 Datetime columns: {len(datetime)}")

# ====PHASE DATA QUALITY CHECK===
print("\n"+"="*50)
print("DATA QUALITY CHECK")
print("="*50)

# 1. missing values
print("\n📛 Missing Values:")
missing = df.isnull().sum()
missing_pct = ((missing / len(df)) * 100).round(2)
missing_df = pd.DataFrame({
    'missing_count': missing, 
    'percent':missing_pct
    }).sort_values(by='percent', ascending=False)

if missing_df['missing_count'].sum() == 0:
    print("✅ No missing values found.")
else:
    print(missing_df[missing_df['missing_count'] > 0])

# 2. Duplicate 
print("\n📛 Duplicate Rows:")
duplicates = df.duplicated().sum()
print(f" Exact duplicate rows: {duplicates:,}({(duplicates/len(df)*100):.2f}%)")

if 'market' in df.columns and 'market_size' in df.columns:
    id_duplicates = df.duplicated(subset=['market', 'market_size']).sum()
    print(f" Duplicate IDS:{id_duplicates:,}")
if duplicates == 0:
    print("✅ No duplicate rows found.")
else:
    print(f"⚠️ {duplicates} duplicate rows found.")

# 3.data types
print("\n📛 Data Types Check:")

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

print(f"\n✅ Numerical columns validated: {len(numerical_cols)}:{numerical_cols}")
print(f"\n✅ Categorical columns validated: {len(categorical_cols)}:{categorical_cols}")
print(f"\n✅ Datetime columns validated: {len(datetime_cols)}:{datetime_cols}")
print(f" ALL types validated ✅")

# 4.CHECK FOR MISCLASSIFIED DATA TYPES
print("\n📛 Misclassified Data Types Check:")

for col in df.columns:
    # check if 'numeric'column stored as object
    if df[col].dtype == 'object':
        # try to convert to numeric
        try:
            numeric_version = pd.to_numeric(df[col], errors='raise')
            non_null_original = df[col].notnull().sum()
            non_null_converted = numeric_version.notnull().sum()
            if non_null_converted / non_null_original >0.95:
                print(f"⚠️ Column '{col}' may be misclassified. Consider converting to numeric.")
            pd.to_datetime(df[col])
            print(f"⚠️ Column '{col}' may be misclassified. Consider converting to datetime.")
        except (ValueError, TypeError):
            pass
    elif df[col].dtype in ['int64', 'float64']:
        unique_values = df[col].nunique()
        if unique_values < 20:
            print(f"⚠️ Column '{col}' may be misclassified. Consider converting to categorical.")

# convert 'date' columns
for col in df.columns:
    if 'date' in col.lower():
        try:
            df[col] = pd.to_datetime(df[col])
            print(f"🔄 Converted column '{col}' to datetime.")
        except (ValueError, TypeError):
            print(f"❌ Failed to convert column '{col}' to datetime.")

# data frame groupby inspections
print("\n"+"="*50)
print("DATA FRAME GROUPBY INSPECTIONS")
print("="*50)

# Example 1: Simple aggregation with groupby
info_cols_detail = df.groupby('Market Size').agg(
    total_records = ('Area Code', 'count'),
    total_profit = ('Profit', 'sum'),
    avg_sales = ('Sales', 'mean')
)
print("\n📊 Grouped Data by Market Size:")
print(info_cols_detail)

# Example 2: Using sum() with groupby and unstack() for pivot-like view
# Group by two columns and use unstack to pivot
profit_by_state_market = df.groupby(['State', 'Market Size'])['Profit'].sum().unstack(fill_value=0)
print("\n📊 Total Profit by State and Market Size (using sum() and unstack()):")
print(profit_by_state_market)

# Example 3: Multiple aggregations with unstack
sales_summary = df.groupby(['State', 'Product Type']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).unstack(fill_value=0)
print("\n📊 Sales & Profit Summary (Multi-level with unstack()):")
print(sales_summary.head())

print("data inspection completed📌")