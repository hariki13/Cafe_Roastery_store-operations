# store-operations
Coffee Roastery Operations - Data Analysis & Analytics System

## Overview
This project provides comprehensive data analysis and analytics tools for coffee shop and specialty coffee roastery operations. The system is designed to help optimize operations through data-driven insights.

## Features

### Data Cleaning
- Automatic datetime conversion and validation
- Missing value detection and removal
- Duplicate row elimination
- Negative value validation for sales data

### Descriptive Analytics
- Sales statistics (total, average, median, standard deviation, min, max)
- Quartile analysis (Q1, Q3, IQR)
- Top products analysis by sales volume and quantity sold

### Time-Based Analytics
- Hourly sales patterns to identify peak hours
- Day of week analysis to determine best sales days
- Monthly sales trends
- Daily sales trend visualization

### Payment Method Analysis
- Sales breakdown by payment type (cash, card)
- Transaction counts and average values per payment method
- Percentage distribution of payment methods

### Visualizations Generated
1. **Top 5 Products by Sales** - Bar chart showing best-selling products by revenue
2. **Top 5 Products by Items Sold** - Bar chart showing most popular products by quantity
3. **Daily Sales Trend** - Line chart showing sales over time
4. **Hourly Sales Pattern** - Bar chart showing sales by hour of day
5. **Day of Week Sales** - Bar chart comparing sales across weekdays
6. **Sales Distribution** - Histogram with mean and median markers
7. **Payment Method Distribution** - Pie chart (if payment data available)

## Requirements
- Python 3.x
- pandas
- matplotlib
- seaborn
- numpy

## Usage
1. Place your data file as `coffee sales dataset.csv` in the project directory
2. Run the analysis script:
   ```bash
   python "project 1 cleaning,descriptive analytics.py"
   ```
3. View the generated reports and visualization files

## Output Files
- `project1 cleaning,descriptive analytics.csv` - Cleaned dataset
- `*.png` - Visualization charts

## Data Format
The input CSV file should contain the following columns:
- `datetime` - Transaction timestamp
- `money` - Transaction amount
- `coffee_name` - Product name
- `cash_type` (optional) - Payment method
