# Store Operations Analytics

**Coffee Shop Operations & Inventory Optimization System**

A comprehensive analytics solution for coffee brands to optimize operations, manage inventory efficiently, and make data-driven decisions.

## Features

### 📊 Data Analysis
- **Data Cleaning**: Automated data validation, type conversion, and duplicate removal
- **Descriptive Statistics**: Total sales, average transactions, transaction counts
- **Product Analysis**: Top products by sales and items sold with percentage breakdowns

### ⏰ Time-Based Analytics
- **Hourly Analysis**: Identify peak hours for staff scheduling and inventory preparation
- **Daily Patterns**: Understand busiest and slowest days of the week
- **Weekly/Monthly Trends**: Track longer-term patterns with moving averages
- **Trend Smoothing**: 7-day moving average for clearer trend visualization

### 📦 Inventory Optimization
- **Product Velocity**: Calculate daily sales velocity for each product
- **Stock Level Recommendations**: Identify high-demand products for restocking priority
- **Low Performers**: Flag slow-moving products for review or discontinuation
- **Peak Demand Forecasting**: Product-specific peak hour analysis

### 💰 Customer Insights
- **Transaction Segmentation**: Group transactions by value (Low, Medium, High, Premium)
- **Payment Method Analysis**: Understand payment preferences
- **Revenue Share Analysis**: Identify top revenue contributors

### 📈 Visualizations
- Top products by sales and items sold
- Hourly sales patterns with peak hour markers
- Daily sales trends with moving average overlay
- Weekly comparison with busiest day highlight
- Product velocity chart with priority classification

## Installation

### Requirements
- Python 3.8+
- pandas
- matplotlib
- seaborn
- numpy

### Install Dependencies
```bash
pip install pandas matplotlib seaborn numpy
```

## Usage

### Quick Start
```python
from analytics import CoffeeAnalytics

# Initialize and run full analysis
analytics = CoffeeAnalytics('your_sales_data.csv')
analytics.load_data()
analytics.clean_data()
analytics.run_full_analysis()
```

### Generate Sample Data (for testing)
```python
from sample_data_generator import generate_sample_data

# Generate 1000 sample transactions over 90 days
df = generate_sample_data(num_records=1000, days=90)
```

### Individual Analysis Methods
```python
# Get descriptive statistics
stats = analytics.get_descriptive_stats()

# Analyze peak hours
hourly = analytics.analyze_hourly_sales()
print(f"Peak hours: {hourly['peak_hours']}")

# Get inventory recommendations
inventory = analytics.get_inventory_recommendations()
print(inventory['insights'])

# Analyze products
products = analytics.analyze_products(top_n=10)

# Generate visualizations only
analytics.plot_top_products()
analytics.plot_hourly_analysis()
analytics.plot_daily_trends()
analytics.plot_weekly_comparison()
analytics.plot_inventory_velocity()

# Export to CSV
analytics.export_analysis_to_csv(prefix='my_analysis')
```

## Data Format

The input CSV file should contain the following columns:
- `datetime`: Transaction timestamp (YYYY-MM-DD HH:MM:SS)
- `coffee_name`: Product name
- `money`: Transaction amount
- `cash_type` (optional): Payment method

## Output Files

When running full analysis, the following files are generated:

### Visualizations (PNG)
- `top_products_analysis.png` - Top products by sales and items sold
- `hourly_sales_analysis.png` - Sales by hour with peak hours marked
- `daily_sales_trend.png` - Daily sales with 7-day moving average
- `weekly_sales_comparison.png` - Sales by day of week
- `product_velocity.png` - Product velocity for inventory management

### CSV Reports
- `analysis_cleaned_data.csv` - Cleaned dataset with extracted features
- `analysis_products.csv` - Product performance analysis
- `analysis_hourly_stats.csv` - Hourly statistics
- `analysis_daily_stats.csv` - Daily statistics by day of week
- `analysis_product_velocity.csv` - Product velocity data

## Example Report Output

```
============================================================
COFFEE OPERATIONS ANALYTICS REPORT
============================================================

--- SALES OVERVIEW ---
Total Revenue: $4,310.00
Total Transactions: 1,000
Average Transaction: $4.31
Unique Products: 15

--- PEAK HOURS ANALYSIS ---
Peak Hours: [8, 7, 15]
Slow Hours: [3, 22, 2]
Recommendation: Peak hours: [8, 7, 15]. Consider extra staffing and inventory during these times.

--- DAILY PATTERNS ---
Busiest Day: Friday
Slowest Day: Sunday

--- TOP 5 PRODUCTS BY SALES ---
  Iced Latte: $455.26 (10.56%)
  Caramel Frappuccino: $445.83 (10.34%)
  Latte: $417.59 (9.69%)

--- INVENTORY RECOMMENDATIONS ---
  • High-demand products: Ensure adequate stock levels
  • Low-demand products: Review pricing or phase out
============================================================
```

## Project Structure

```
store-operations/
├── README.md                              # This file
├── analytics.py                           # Main analytics module
├── sample_data_generator.py               # Sample data generator for testing
├── project 1 cleaning,descriptive analytics.py  # Original basic analysis script
└── .gitignore                             # Git ignore configuration
```

## License

MIT License
