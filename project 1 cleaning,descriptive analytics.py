# --- Step 1: Import Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Step 2: Load Your Data ---
df = pd.read_csv('coffee sales dataset.csv')
print("=" * 60)
print("COFFEE ROASTERY OPERATIONS - DATA ANALYSIS REPORT")
print("=" * 60)
print("\n--- Initial Data Overview ---")

# step 3. Preview the data first 5 rows
print("1. First 5 Rows of the dataset:")
print(df.head())

# step 4. Get a concise summary the dataframe, including data types and non-null values
print("\n2. Data Types and Non-Null Values:")
df.info()

# step 5. Data Cleaning ---
print("\n--- Starting Data Cleaning ---")

# Convert 'datetime' column from object to datetime type for time-series analysis
# The errors = 'coerce' will turn any values that can't be converted into NaT (Not a Time)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Check for missing values after conversion
print("\n3. Missing Values in each column after conversion:")
print(df.isnull().sum())

# Validate money column - remove negative values and outliers
if 'money' in df.columns:
    invalid_money = (df['money'] < 0).sum()
    if invalid_money > 0:
        print(f"\n4. Removed {invalid_money} rows with negative money values.")
        df = df[df['money'] >= 0]

# Remove rows where 'datetime' or 'money' is missing, as they are critical for analysis
df.dropna(subset=['datetime', 'money', 'coffee_name'], inplace=True)

# Remove duplicate rows to ensure data accuracy
initial_rows = len(df)
df.drop_duplicates(inplace=True)
duplicates_removed = initial_rows - len(df)
print(f"\n5. Removed {duplicates_removed} duplicate rows.")
print(f"   Final dataset size: {len(df)} rows")

# step 6. ---- Descriptive Analytics ----
print("\n" + "=" * 60)
print("DESCRIPTIVE ANALYTICS")
print("=" * 60)

# Calculate basic statistics for the 'money' column
total_sales = df['money'].sum()
average_sales = df['money'].mean()
max_sales = df['money'].max()
min_sales = df['money'].min()
std_sales = df['money'].std()
median_sales = df['money'].median()

print(f"\n1. Sales Statistics:")
print(f"   Total Sales: ${total_sales:,.2f}")
print(f"   Average Sale: ${average_sales:.2f}")
print(f"   Median Sale: ${median_sales:.2f}")
print(f"   Standard Deviation: ${std_sales:.2f}")
print(f"   Maximum Sale: ${max_sales:.2f}")
print(f"   Minimum Sale: ${min_sales:.2f}")

# Quartile analysis
q1 = df['money'].quantile(0.25)
q3 = df['money'].quantile(0.75)
iqr = q3 - q1
print(f"\n2. Quartile Analysis:")
print(f"   25th Percentile (Q1): ${q1:.2f}")
print(f"   75th Percentile (Q3): ${q3:.2f}")
print(f"   Interquartile Range (IQR): ${iqr:.2f}")

# step 7. Analyze product sales
# Group by coffee name and calculate total sales and number of items sold for each
product_analysis = df.groupby('coffee_name')['money'].agg(['sum', 'count', 'mean']).reset_index()
product_analysis.rename(columns={'sum': 'total_sales', 'count': 'items_sold', 'mean': 'avg_price'}, inplace=True)

# Find the top 5 products by Sales
top_5_products_by_sales = product_analysis.sort_values(by='total_sales', ascending=False).head(5)
print("\n3. Top 5 Products by Total Sales:")
print(top_5_products_by_sales.to_string(index=False))

# Find the top 5 products by items sold
top_5_products_by_items_sold = product_analysis.sort_values(by='items_sold', ascending=False).head(5)
print("\n4. Top 5 Products by Items Sold:")
print(top_5_products_by_items_sold.to_string(index=False))

# --- Step 7a: Time-Based Analytics ---
print("\n" + "=" * 60)
print("TIME-BASED ANALYTICS")
print("=" * 60)

# Extract time components for analysis
df['hour'] = df['datetime'].dt.hour
df['day_of_week'] = df['datetime'].dt.day_name()
df['month'] = df['datetime'].dt.month_name()
df['date'] = df['datetime'].dt.date

# Constants
UNKNOWN_DAY_ORDER = 7

# Hourly sales analysis
hourly_sales = df.groupby('hour')['money'].agg(['sum', 'count']).reset_index()
hourly_sales.rename(columns={'sum': 'total_sales', 'count': 'transactions'}, inplace=True)

peak_hour = None
if not hourly_sales.empty:
    peak_hour = hourly_sales.loc[hourly_sales['total_sales'].idxmax(), 'hour']
    print(f"\n5. Peak Sales Hour: {int(peak_hour)}:00 - {int(peak_hour)+1}:00")
else:
    print("\n5. Peak Sales Hour: No hourly data available")

# Day of week analysis
daily_pattern = df.groupby('day_of_week')['money'].agg(['sum', 'count']).reset_index()
daily_pattern.rename(columns={'sum': 'total_sales', 'count': 'transactions'}, inplace=True)
# Sort by weekday order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_pattern['day_order'] = daily_pattern['day_of_week'].apply(lambda x: day_order.index(x) if x in day_order else UNKNOWN_DAY_ORDER)
daily_pattern = daily_pattern.sort_values('day_order')

best_day = None
if not daily_pattern.empty:
    best_day = daily_pattern.loc[daily_pattern['total_sales'].idxmax(), 'day_of_week']
    print(f"\n6. Best Sales Day: {best_day}")
else:
    print("\n6. Best Sales Day: No daily data available")

print("\n   Sales by Day of Week:")
for _, row in daily_pattern.iterrows():
    print(f"   {row['day_of_week']}: ${row['total_sales']:,.2f} ({row['transactions']} transactions)")

# Monthly analysis
monthly_sales = df.groupby('month')['money'].agg(['sum', 'count']).reset_index()
monthly_sales.rename(columns={'sum': 'total_sales', 'count': 'transactions'}, inplace=True)
print("\n7. Monthly Sales Summary:")
print(monthly_sales.to_string(index=False))

# --- Step 7b: Payment Method Analysis (if available) ---
if 'cash_type' in df.columns:
    print("\n" + "=" * 60)
    print("PAYMENT METHOD ANALYSIS")
    print("=" * 60)
    
    payment_analysis = df.groupby('cash_type')['money'].agg(['sum', 'count', 'mean']).reset_index()
    payment_analysis.rename(columns={'sum': 'total_sales', 'count': 'transactions', 'mean': 'avg_transaction'}, inplace=True)
    payment_analysis['percentage'] = (payment_analysis['total_sales'] / total_sales * 100).round(2)
    
    print("\n8. Sales by Payment Method:")
    print(payment_analysis.to_string(index=False))

# --- step 8: Visualizations ----
print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)

# Set the style for the plots
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 100

# a. Bar chart for top 5 products by sales
plt.figure(figsize=(10, 6))
sns.barplot(x='total_sales', y='coffee_name', data=top_5_products_by_sales, color='red')
plt.title('Top 5 Products by Sales', fontsize=16)
plt.xlabel('Total Sales ($)', fontsize=12)
plt.ylabel('Product', fontsize=12)
plt.tight_layout()
plt.savefig('top_5_products_by_sales.png')
print("\n1. Saved 'top_5_products_by_sales.png'")

# b. Bar chart for top 5 products by items sold
plt.figure(figsize=(10, 6))
sns.barplot(x='items_sold', y='coffee_name', data=top_5_products_by_items_sold, color='green')
plt.title('Top 5 Products by Items Sold', fontsize=16)
plt.xlabel('Items Sold', fontsize=12)
plt.ylabel('Product', fontsize=12)
plt.tight_layout()
plt.savefig('top_5_products_by_items_sold.png')
print("2. Saved 'top_5_products_by_items_sold.png'")

# c. Daily Sales Trend
# Resample data by day and sum the 'money' to get daily sales
daily_sales = df.set_index('datetime').resample('D')['money'].sum()

plt.figure(figsize=(14, 7))
daily_sales.plot(kind='line', marker='o', color='blue', linestyle='--', linewidth=2)
plt.title('Daily Sales Trend', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('daily_sales_trend.png')
print("3. Saved 'daily_sales_trend.png'")

# d. Hourly Sales Pattern
plt.figure(figsize=(12, 6))
sns.barplot(x='hour', y='total_sales', data=hourly_sales, color='purple')
plt.title('Sales by Hour of Day', fontsize=16)
plt.xlabel('Hour', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.tight_layout()
plt.savefig('hourly_sales_pattern.png')
print("4. Saved 'hourly_sales_pattern.png'")

# e. Day of Week Sales Pattern
plt.figure(figsize=(12, 6))
sns.barplot(x='day_of_week', y='total_sales', data=daily_pattern, order=day_order, color='orange')
plt.title('Sales by Day of Week', fontsize=16)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('day_of_week_sales.png')
print("5. Saved 'day_of_week_sales.png'")

# f. Sales Distribution Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['money'], bins=30, color='teal', edgecolor='black', alpha=0.7)
plt.axvline(average_sales, color='red', linestyle='dashed', linewidth=2, label=f'Mean: ${average_sales:.2f}')
plt.axvline(median_sales, color='green', linestyle='dashed', linewidth=2, label=f'Median: ${median_sales:.2f}')
plt.title('Sales Distribution', fontsize=16)
plt.xlabel('Sale Amount ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('sales_distribution.png')
print("6. Saved 'sales_distribution.png'")

# g. Payment Method Pie Chart (if available)
if 'cash_type' in df.columns:
    plt.figure(figsize=(8, 8))
    payment_totals = df.groupby('cash_type')['money'].sum()
    plt.pie(payment_totals, labels=payment_totals.index, autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('pastel'))
    plt.title('Sales by Payment Method', fontsize=16)
    plt.tight_layout()
    plt.savefig('payment_method_distribution.png')
    print("7. Saved 'payment_method_distribution.png'")

# Save cleaned data to CSV
df.to_csv("project1 cleaning,descriptive analytics.csv", index=False)
print("\n8. Saved cleaned data to 'project1 cleaning,descriptive analytics.csv'")

# --- Final Summary ---
print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"\nTotal transactions analyzed: {len(df)}")
print(f"Total revenue: ${total_sales:,.2f}")
print(f"Average transaction value: ${average_sales:.2f}")
if peak_hour is not None:
    print(f"Peak sales hour: {int(peak_hour)}:00")
else:
    print("Peak sales hour: N/A")
if best_day is not None:
    print(f"Best sales day: {best_day}")
else:
    print("Best sales day: N/A")
print(f"\nVisualization files generated:")
print("  - top_5_products_by_sales.png")
print("  - top_5_products_by_items_sold.png")
print("  - daily_sales_trend.png")
print("  - hourly_sales_pattern.png")
print("  - day_of_week_sales.png")
print("  - sales_distribution.png")
if 'cash_type' in df.columns:
    print("  - payment_method_distribution.png")
print("\n## To see the plots, open the saved .png files")
print("## or add 'plt.show()' after each plot section.")
