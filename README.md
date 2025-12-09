# store-operations
Coffeeshop, Specialty Coffeeshop, WARKOP System - Optimize the Operations

## Modules

### 1. Project 1: Coffee Sales Analytics
- Data cleaning and descriptive analytics for coffee sales
- Top products analysis by sales and items sold
- Daily sales trend visualization

### 2. Coffee Roastery Management
The `coffee_roastery.py` module provides comprehensive functionality for managing coffee roastery operations:

#### Features:
- **Cost Calculation**: Track green bean costs, roasting costs, and calculate total cost per kg of roasted coffee
- **Inventory Management**: Manage both green bean and roasted bean inventories with FIFO costing
- **Weight Loss Tracking**: Calculate and report weight loss during roasting (typically 12-20% depending on roast level)
- **Pricing Calculator**: Calculate suggested selling prices based on costs and desired profit margins

#### Key Concepts:
- Green coffee beans lose weight during roasting due to moisture loss and chemical changes
- Light roasts typically have ~13% weight loss
- Medium roasts typically have ~15% weight loss  
- Dark roasts typically have ~18% weight loss
- Cost per kg of roasted coffee must account for this weight loss

#### Usage Example:
```python
from coffee_roastery import CoffeeRoastery

# Create a roastery instance
roastery = CoffeeRoastery()

# Add green beans to inventory
roastery.add_green_beans(
    bean_type='Ethiopian Yirgacheffe',
    quantity_kg=50,
    cost_per_kg=15.00,
    supplier='African Coffee Traders'
)

# Roast beans and record the batch
result = roastery.roast_beans(
    bean_type='Ethiopian Yirgacheffe',
    green_bean_kg=10,
    roasted_bean_kg=8.7,  # 13% weight loss
    roasting_cost=25.00,
    roast_level='light'
)

# Get reports
weight_report = roastery.get_weight_loss_report()
cost_report = roastery.get_cost_report()

# Calculate selling price with 40% profit margin
pricing = roastery.calculate_selling_price(
    cost_per_kg_roasted=19.23,
    profit_margin_percent=40
)
```

#### Methods:
- `add_green_beans()` - Add green beans to inventory
- `roast_beans()` - Record a roasting batch and update inventories
- `calculate_weight_loss()` - Calculate weight loss during roasting
- `estimate_roasted_weight()` - Estimate roasted weight based on expected loss
- `get_green_bean_inventory_summary()` - Summary of green bean inventory
- `get_roasted_bean_inventory_summary()` - Summary of roasted bean inventory
- `get_weight_loss_report()` - Report on weight loss across all batches
- `get_cost_report()` - Cost breakdown report
- `calculate_selling_price()` - Calculate selling price with profit margin
- `export_to_csv()` - Export all data to CSV files

## Requirements
- pandas
- matplotlib
- seaborn
