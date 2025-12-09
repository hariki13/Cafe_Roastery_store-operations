# Store Operations
Coffeeshop, Specialty Coffeeshop, WARKOP System - Optimize the Operations

## Overview
This repository contains data analysis tools for coffee shop and roastery operations, including sales analytics and pricing decision support based on cost operations.

## Project Files

### 1. Sales Analytics (`project 1 cleaning,descriptive analytics.py`)
Data cleaning and descriptive analytics for coffee sales data:
- Data loading and cleaning
- Sales trend analysis
- Top products by sales and volume
- Daily sales visualization

### 2. Cost & Pricing Analysis (`project2_cost_pricing_analysis.py`)
Comprehensive cost operations and pricing decision analysis:
- **Cost Breakdown Analysis**: Raw materials, labor, and overhead costs per product
- **Profitability Analysis**: Profit margins and markup percentages
- **Break-Even Analysis**: Calculate break-even point in units and revenue
- **Pricing Recommendations**: Target margin pricing strategies (50%, 60%, cost-plus)
- **Financial Summary**: Monthly revenue, costs, and profit projections

## Requirements
```
pandas
matplotlib
seaborn
numpy
```

Install dependencies:
```bash
pip install pandas matplotlib seaborn numpy
```

## Usage

### Run Sales Analytics
```bash
python "project 1 cleaning,descriptive analytics.py"
```

### Run Cost & Pricing Analysis
```bash
python project2_cost_pricing_analysis.py
```

## Generated Outputs

The cost pricing analysis generates:
- `cost_breakdown_analysis.png` - Cost structure vs selling price visualization
- `profit_margin_analysis.png` - Profit margin by product
- `monthly_profit_contribution.png` - Monthly profit contribution chart
- `break_even_analysis.png` - Break-even point visualization
- `cost_structure_overview.png` - Cost structure and revenue distribution
- `cost_pricing_analysis.csv` - Detailed analysis data
- `financial_summary.csv` - Key financial metrics

## Key Metrics

The pricing analysis provides:
- Total cost per drink (raw materials + labor + overhead)
- Profit margin percentage per product
- Break-even point calculation
- Recommended prices at target margins
- Monthly financial projections
