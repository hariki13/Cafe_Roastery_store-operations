# store-operations
Coffeeshop, Specialty Coffeeshop, WARKOP System - Optimize the Operations

## Overview
This repository contains data analysis tools for coffee shop operations optimization, including sales analytics and staffing recommendations based on traffic patterns.

## Features

### 1. Data Cleaning & Descriptive Analytics
**File:** `project 1 cleaning,descriptive analytics.py`

- Data loading and cleaning
- Sales statistics (total, average, max, min)
- Product analysis (top products by sales and items sold)
- Daily sales trend visualization

### 2. Staffing Operations Analysis
**File:** `staffing_analysis.py`

Analyzes sales data to identify peak and low traffic hours, providing data-driven staffing recommendations.

**Features:**
- **Hourly Traffic Analysis:** Identifies transaction patterns by hour
- **Peak/Low Hour Classification:** Categorizes hours based on traffic levels
- **Day of Week Analysis:** Shows which days are busiest
- **Staffing Recommendations:** Suggests optimal staff numbers per hour
- **Visualizations:** Generates charts showing traffic patterns and staffing needs

**Output:**
- `staffing_analysis.png` - Visual dashboard with 4 charts
- `staffing_hourly_analysis.csv` - Detailed hourly analysis data
- `staffing_daily_analysis.csv` - Day of week analysis data

## Usage

### Prerequisites
```bash
pip install pandas matplotlib seaborn numpy
```

### Running the Analysis

**Descriptive Analytics:**
```bash
python "project 1 cleaning,descriptive analytics.py"
```

**Staffing Analysis:**
```bash
python staffing_analysis.py
```

## Data Format
The analysis expects a CSV file named `coffee sales dataset.csv` with the following columns:
- `datetime`: Transaction timestamp
- `coffee_name`: Name of the coffee product
- `money`: Transaction amount

## Staffing Recommendations Logic
- Peak hours (top 25% by transactions): Maximum staff allocation
- Low hours (bottom 25% by transactions): Minimum staff allocation
- Normal hours: Moderate staff allocation
- Base staff level can be configured in the code
