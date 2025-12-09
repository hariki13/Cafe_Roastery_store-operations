# store-operations
Coffeeshop, Specialty Coffeeshop, WARKOP System - Optimize Store Operations

A comprehensive data analytics suite for coffee shop and roastery operations, including sales analysis and coffee roasting data analytics.

## Features

### Coffee Sales Analytics (`project 1 cleaning,descriptive analytics.py`)
- Data cleaning and preprocessing for coffee sales data
- Descriptive analytics for sales metrics
- Product performance analysis (top sellers by revenue and quantity)
- Daily sales trend visualization

### Coffee Roasting Analytics (`coffee_roasting_analytics.py`)
- Coffee roast profile data analysis
- Quality metrics tracking (cupping scores, Agtron readings)
- Bean origin performance comparison
- Roaster performance analysis
- Key visualizations:
  - Cupping score distribution
  - Quality by bean origin
  - Roast time vs quality correlation
  - Weight loss by roast level
  - Development time ratio analysis
  - Monthly production trends
  - Roasting parameters correlation heatmap

## Installation

```bash
pip install pandas matplotlib seaborn numpy
```

## Usage

### Coffee Sales Analytics
```bash
# Requires: 'coffee sales dataset.csv' in the working directory
python "project 1 cleaning,descriptive analytics.py"
```

### Coffee Roasting Analytics
```bash
# Uses sample data by default, or load your own roasting data
python coffee_roasting_analytics.py
```

## Output Files

The roasting analytics module generates:
- `coffee_roasting_data_cleaned.csv` - Cleaned roasting data
- `cupping_score_distribution.png` - Quality score distribution
- `cupping_score_by_origin.png` - Quality by origin
- `roast_time_vs_quality.png` - Time-quality correlation
- `weight_loss_by_roast_level.png` - Weight loss analysis
- `dtr_vs_quality.png` - Development time ratio analysis
- `monthly_production_trend.png` - Production trends
- `roasting_parameters_correlation.png` - Parameter correlations

## Data Format

### Roasting Data Columns
- `batch_id`: Unique batch identifier
- `roast_date`: Date of roasting
- `bean_origin`: Coffee bean origin country
- `green_bean_weight_kg`: Weight of green beans (kg)
- `roast_level`: Light, Medium-Light, Medium, Medium-Dark, Dark
- `charge_temp_celsius`: Initial roasting temperature
- `first_crack_temp_celsius`: Temperature at first crack
- `first_crack_time_min`: Time to first crack (minutes)
- `drop_temp_celsius`: Final/drop temperature
- `total_roast_time_min`: Total roasting time (minutes)
- `development_time_ratio`: Post-first-crack development ratio
- `weight_loss_percent`: Percentage of weight loss during roasting
- `agtron_score`: Agtron color reading (roast darkness)
- `cupping_score`: SCA cupping score (0-100)
- `roaster_id`: Roaster identifier
