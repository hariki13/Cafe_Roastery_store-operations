# Store Operations - Specialty Coffee Shop Analytics

Comprehensive data analysis and analytics system for specialty coffee shop operations, including bakery and cake products.

## Features

### Basic Analytics (`project 1 cleaning,descriptive analytics.py`)
- Data loading and cleaning
- Basic descriptive statistics
- Top products by sales and quantity
- Daily sales trend visualization

### Enhanced Analytics (`enhanced_analytics.py`)
A comprehensive analytics module with advanced capabilities:

#### Data Processing
- Automated data cleaning and preprocessing
- Datetime parsing and extraction (hour, day, week, month)
- Product categorization (coffee, bakery, cake, other)
- Outlier detection (IQR and Z-score methods)
- Missing value handling

#### Descriptive Statistics
- Count, total, mean, median, mode
- Standard deviation, variance
- Min, max, range
- Quartiles (Q1, Q3, IQR)
- Skewness and kurtosis

#### Business Analytics
- Product performance analysis
- Category-wise breakdown (coffee, bakery, cake)
- Peak hours identification
- Weekend vs weekday comparison
- Sales growth rate calculation
- Time-based analysis (hourly, daily, weekly, monthly)

#### Visualizations
- Sales distribution (histogram and box plot)
- Top products bar charts
- Category breakdown (pie and bar charts)
- Daily sales trend with trend line
- Hourly heatmap by day of week
- Monthly comparison charts

#### Export & Reporting
- CSV, Excel, and JSON export
- Comprehensive report generation
- Automated visualization saving

## Installation

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Usage

### Basic Usage

```python
from enhanced_analytics import CoffeeShopAnalytics

# Initialize with data file
analytics = CoffeeShopAnalytics(data_path='coffee sales dataset.csv')

# Clean data
analytics.clean_data()

# Get descriptive statistics
stats = analytics.get_descriptive_statistics()
print(f"Total Sales: ${stats['total']:,.2f}")

# Analyze by category
categories = analytics.get_category_analysis()
print(categories)

# Generate full report
report = analytics.generate_comprehensive_report(output_dir='reports')
```

### Adding Custom Categories

```python
# Add bakery-specific items
analytics.add_custom_category('pastries', ['croissant', 'danish', 'turnover'])
analytics.add_custom_category('cakes', ['layer cake', 'pound cake', 'wedding cake'])
```

### Running Demo Analysis

```bash
python enhanced_analytics.py
```

## Data Format

The analytics system expects a CSV file with at least the following columns:
- `datetime`: Transaction timestamp
- `coffee_name`: Product name
- `money`: Sale amount

## Output

Generated reports include:
- `top_products.png` - Top selling products
- `category_breakdown.png` - Sales by category
- `daily_trend.png` - Daily sales trend
- `hourly_heatmap.png` - Sales heatmap by hour and day
- `sales_distribution.png` - Distribution analysis
- `cleaned_sales_data.csv` - Cleaned dataset

## Project Structure

```
store-operations/
├── README.md
├── .gitignore
├── project 1 cleaning,descriptive analytics.py  # Basic analytics
├── enhanced_analytics.py                        # Enhanced analytics module
└── coffee sales dataset.csv                     # Sample data (if available)
```

## License

This project is for educational and operational purposes for specialty coffee shop management.
