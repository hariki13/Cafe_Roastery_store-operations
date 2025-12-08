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

# 2. last look - Bottom rows (catched data loading issues)
print("\n📌Last 5 rows:")
print(df.tail())

# 3.RANDOM SAMPLE - Random rows (catch data consistency issues)
print("\n📌Random Sample of 5 rows:")
print(df.sample(5))

# 4.DIMENSIONS - Shape of the data
print(f"\n🔧 dataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

#  5. MEMORY USAGE - Memory usage of the dataframe
print(f"\n💾 memory usage:\n{df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

print("="*50)
print("DATA STRUCTURE DEEP DIVE ANALYSIS")
print("="*50)

# 1. BASIC INFO
print("\n📋 Dataframe Info:")
print(df.info())

# 2. COLUMN ANALYSIS
print(f"\n🔍 Column-wise Analysis: {len(df.columns)} columns")
print("\n column names:")
for i, col in enumerate(df.columns, 1):
    print(f" {i}. {col}")

# 3. DATA TYPES BREAKDOWN
print("\n📊 Data Types Distribution:")
print(df.dtypes.value_counts())

# 4. DETAILED TYPE ANALYSIS
print("\n📡 columns by type:")
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

print(f" ✅ Numerical columns ({len(numerical_cols)}): {numerical_cols}")
print(f"  🟠 Categorical columns ({len(categorical_cols)}): {categorical_cols}")
print(f"  📅 Datetime columns ({len(datetime_cols)}): {datetime_cols}")

print("="*50)
print("PHASE 3: DATA QUALITY CHECK ✅")
print("MISSING VALUES ANALYSIS")
print("="*50)

# 1. OVERALL MISSINGNESS
total_cells = df.shape[0] * df.shape[1]
total_missing = df.isnull().sum().sum()
print(f"\n🖼️ total cells: {total_cells:,}")
print(f"❌ total missing cells: {total_missing:,} ({total_missing / total_cells * 100:.2f}% missing)")

# 2. MISSINGNESS BY COLUMN
missing_df = pd.DataFrame({
    'column': df.columns,
    'missing_count': df.isnull().sum().values,
    'missing_percent': ((df.isnull().sum().values/len(df)) * 100).round(2),
    'data_type': df.dtypes.values
})
# sort ny missing percentage
missing_df = missing_df.sort_values(by='missing_percent', ascending=False)
print("\n📋 Missing Values by Column:")
print(missing_df[missing_df['missing_count'] > 0]. to_string(index=False))

# 3. COLUMNS WITH NO MISSING DATA
complete_cols = missing_df[missing_df['missing_count'] == 0]['column'].tolist()
print(f"\n✅ Columns with no missing data ({len(complete_cols)}): {complete_cols}")

# 4. CRITICAL ASSESSMENT
print("\n🚧 MISSINGNESS SEVERITY ASSESSMENT:")
for i, row in missing_df.iterrows():
    if row['missing_percent'] > 50:
        print(f" ✅ CRITICAL : {row['column']} ({row['missing_percent']:.2f}% missing) - Consider dropping or imputing")
    elif row['missing_percent'] > 20:
        print(f" ⚠️ MODERATE : {row['column']} ({row['missing_percent']:.2f}% missing) - Consider imputation or further investigation")
        status = "⚠️ Low MODERATE missingness"
    elif row['missing_percent'] > 0:
        print(f" ❗ MINOR : {row['column']} ({row['missing_percent']:.2f}% missing) - Monitor but likely acceptable")
        status = "❗ MINOR missingness"
    
    
print("\n✅ Data inspection completed.")

print("="*50)
print("STEP 6: DUPLICATE DETECTION - THOROUGH CHECK")
print("DUPLICATE ANALYSIS")
print("="*50)

# 1. EXACT DUPLICATES (all columns)
exact_duplicates = df.duplicated().sum()
print(f"\n📌 Exact Duplicates rows: {exact_duplicates:,} ({exact_duplicates / len(df) * 100:.2f}% of total rows)")

if exact_duplicates > 0:
    print("\nExample duplicates:")
    print(df[df.duplicated(keep=False)].head(10))

# 2. DUPLICATES IN KEY COLUMNS (CUSTOMIZE AS NEEDED)
if 'IDStore' in df.columns:
    key_duplicates = df.duplicated(subset=['IDStore']).sum()
    print(f"\n📌 Duplicates based on 'IDStore': {key_duplicates:,} ({key_duplicates / len(df) * 100:.2f}% of total rows)")
    
    if key_duplicates > 0:
        print("\nExample key duplicates:")
        print(df[df.duplicated(subset=['IDStore'], keep=False)].head(10))
else:
    print("\n⚠️ 'IDStore' column not found for key duplicate check.")

# 3. DUPLICATES WITH SUBSET (15 columns)
key_cols = df.columns[:15].tolist()
if all(col in df.columns for col in key_cols):
    subset_duplicates = df.duplicated(subset=key_cols).sum()
    print(f"\n📌 Duplicates {' + '.join(key_cols)}: {subset_duplicates:,} ({subset_duplicates / len(df) * 100:.2f}% of total rows)")
else:
    print("\n⚠️ Not all key columns found for subset duplicate check.")


print("=="*50)
print("STEP 7: DATA TYPE VALIDATION-FIX COMMON ISSUES")
print("DATA TYPE VALIDATION")
print("=="*50)

# 1. CHECK FOR MISCLASSIFIED DATA TYPES
print("\n🔍 checking for type issues...:")

for col in df.columns:
    # check if 'numeric' column stored as object
    if df[col].dtype == 'object':
        # Try converting to numeric
        try:
            numeric_version = pd.to_numeric(df[col], errors='coerce')
            non_null_original = df[col].notna().sum()
            non_null_converted = numeric_version.notna().sum()
            
            if non_null_converted / non_null_original > 0.95: # 95% conversion rate successfully
                print(f" 🚧 '{col}' should probably be NUMERIC (currently object)")
        except ValueError:
            pass
        
        # check if date column stored as object
        if df[col].dtype == 'object' and 'date' in col.lower():
            print(f" 🚧 '{col} might be a DATE (currently object)")

try:
    # Convert multiple datetime columns
    for col in ['opentime', 'closedtime']:
        df[col] = pd.to_datetime(df[col])
        print(f" ✅ Converted column '{col}' to datetime")
except ValueError as e:
    print(f" ❌ Error converting to datetime: {e}")

print("\n✅ Data type validation completed.")