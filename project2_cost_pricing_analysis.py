# --- Cost Operations and Pricing Decision Analysis ---
# This script analyzes cost operations for coffeeshop and roastery
# to support pricing decisions based on operational costs

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Step 1: Define Cost Structure ---
# Cost data for coffee products (per unit in dollars)
# This includes raw materials, labor, and overhead costs

cost_data = {
    'coffee_name': [
        'Espresso', 'Americano', 'Cappuccino', 'Latte', 'Mocha',
        'Macchiato', 'Flat White', 'Cold Brew', 'Iced Coffee', 'Drip Coffee',
        'Cortado', 'Affogato', 'Irish Coffee', 'Turkish Coffee', 'Vienna Coffee'
    ],
    # Raw material costs (coffee beans, milk, syrups, cups, etc.)
    'raw_material_cost': [
        0.45, 0.50, 0.75, 0.80, 0.95,
        0.55, 0.70, 0.60, 0.55, 0.40,
        0.60, 1.10, 1.50, 0.50, 0.90
    ],
    # Labor cost per drink (preparation time * hourly wage / drinks per hour)
    'labor_cost': [
        0.30, 0.35, 0.45, 0.45, 0.50,
        0.35, 0.40, 0.25, 0.25, 0.20,
        0.35, 0.55, 0.60, 0.45, 0.50
    ],
    # Overhead cost allocation per drink (rent, utilities, equipment, etc.)
    'overhead_cost': [
        0.25, 0.25, 0.30, 0.30, 0.35,
        0.25, 0.28, 0.22, 0.22, 0.20,
        0.25, 0.35, 0.40, 0.30, 0.35
    ],
    # Current selling price
    'selling_price': [
        2.50, 2.75, 3.50, 3.75, 4.25,
        3.00, 3.50, 3.25, 3.00, 2.25,
        3.25, 4.50, 5.50, 3.00, 4.00
    ],
    # Estimated monthly sales volume
    'monthly_sales_volume': [
        800, 600, 900, 1200, 500,
        400, 450, 700, 650, 1000,
        300, 200, 150, 250, 180
    ]
}

# Create DataFrame
df_costs = pd.DataFrame(cost_data)

# --- Step 2: Calculate Total Costs and Margins ---
print("=" * 60)
print("COFFEESHOP & ROASTERY COST OPERATIONS ANALYSIS")
print("=" * 60)

# Calculate total cost per unit
df_costs['total_cost'] = (df_costs['raw_material_cost'] + 
                          df_costs['labor_cost'] + 
                          df_costs['overhead_cost'])

# Calculate profit per unit
df_costs['profit_per_unit'] = df_costs['selling_price'] - df_costs['total_cost']

# Calculate profit margin percentage
df_costs['profit_margin_pct'] = (df_costs['profit_per_unit'] / df_costs['selling_price']) * 100

# Calculate markup percentage (from cost)
df_costs['markup_pct'] = ((df_costs['selling_price'] - df_costs['total_cost']) / 
                          df_costs['total_cost']) * 100

# Calculate total monthly revenue and profit
df_costs['monthly_revenue'] = df_costs['selling_price'] * df_costs['monthly_sales_volume']
df_costs['monthly_profit'] = df_costs['profit_per_unit'] * df_costs['monthly_sales_volume']
df_costs['monthly_cost'] = df_costs['total_cost'] * df_costs['monthly_sales_volume']

# --- Step 3: Display Cost Analysis Results ---
print("\n1. COST BREAKDOWN PER PRODUCT")
print("-" * 60)
cost_summary = df_costs[['coffee_name', 'raw_material_cost', 'labor_cost', 
                         'overhead_cost', 'total_cost', 'selling_price']].copy()
cost_summary = cost_summary.round(2)
print(cost_summary.to_string(index=False))

print("\n2. PROFITABILITY ANALYSIS")
print("-" * 60)
profit_summary = df_costs[['coffee_name', 'total_cost', 'selling_price', 
                           'profit_per_unit', 'profit_margin_pct', 'markup_pct']].copy()
profit_summary = profit_summary.round(2)
print(profit_summary.to_string(index=False))

# --- Step 4: Break-Even Analysis ---
print("\n3. BREAK-EVEN ANALYSIS")
print("-" * 60)

# Fixed monthly costs for the coffee shop
fixed_costs = {
    'rent': 3500,
    'utilities': 800,
    'insurance': 300,
    'equipment_depreciation': 400,
    'marketing': 500,
    'licenses_permits': 100,
    'miscellaneous': 400
}

total_fixed_costs = sum(fixed_costs.values())
print(f"Total Monthly Fixed Costs: ${total_fixed_costs:,.2f}")

# Calculate weighted average contribution margin
total_sales_volume = df_costs['monthly_sales_volume'].sum()
df_costs['sales_mix'] = df_costs['monthly_sales_volume'] / total_sales_volume
df_costs['weighted_contribution'] = df_costs['profit_per_unit'] * df_costs['sales_mix']
weighted_avg_contribution = df_costs['weighted_contribution'].sum()

print(f"Weighted Average Contribution Margin: ${weighted_avg_contribution:.2f}")

# Break-even point in units
break_even_units = total_fixed_costs / weighted_avg_contribution
print(f"Break-Even Point (units): {break_even_units:,.0f} drinks/month")

# Break-even point in revenue
weighted_avg_price = (df_costs['selling_price'] * df_costs['sales_mix']).sum()
break_even_revenue = break_even_units * weighted_avg_price
print(f"Break-Even Point (revenue): ${break_even_revenue:,.2f}/month")

# --- Step 5: Pricing Recommendations ---
print("\n4. PRICING RECOMMENDATIONS")
print("-" * 60)

# Target profit margin of 60% for specialty drinks, 50% for standard drinks
df_costs['recommended_price_60pct'] = df_costs['total_cost'] / (1 - 0.60)
df_costs['recommended_price_50pct'] = df_costs['total_cost'] / (1 - 0.50)

# Cost-plus pricing (100% markup)
df_costs['cost_plus_price'] = df_costs['total_cost'] * 2

pricing_recommendations = df_costs[['coffee_name', 'total_cost', 'selling_price',
                                    'recommended_price_50pct', 'recommended_price_60pct',
                                    'cost_plus_price']].copy()
pricing_recommendations.columns = ['Product', 'Cost', 'Current Price', 
                                   'Target 50% Margin', 'Target 60% Margin', 
                                   'Cost-Plus (100%)']
pricing_recommendations = pricing_recommendations.round(2)
print(pricing_recommendations.to_string(index=False))

# --- Step 6: Identify Products Needing Price Adjustment ---
print("\n5. PRODUCTS NEEDING PRICE ADJUSTMENT")
print("-" * 60)

# Products with margin below 40% need attention
low_margin_products = df_costs[df_costs['profit_margin_pct'] < 40][
    ['coffee_name', 'selling_price', 'total_cost', 'profit_margin_pct']
].copy()

if len(low_margin_products) > 0:
    print("Products with profit margin below 40%:")
    print(low_margin_products.to_string(index=False))
else:
    print("All products have healthy profit margins (>=40%)")

# Products with highest profit contribution
print("\n6. TOP PROFIT CONTRIBUTORS")
print("-" * 60)
top_profit = df_costs.nlargest(5, 'monthly_profit')[
    ['coffee_name', 'monthly_sales_volume', 'profit_per_unit', 'monthly_profit']
].copy()
top_profit['monthly_profit'] = top_profit['monthly_profit'].apply(lambda x: f"${x:,.2f}")
print(top_profit.to_string(index=False))

# --- Step 7: Summary Statistics ---
print("\n7. MONTHLY FINANCIAL SUMMARY")
print("-" * 60)
total_monthly_revenue = df_costs['monthly_revenue'].sum()
total_monthly_cost = df_costs['monthly_cost'].sum()
total_monthly_profit = df_costs['monthly_profit'].sum()
overall_margin = (total_monthly_profit / total_monthly_revenue) * 100

print(f"Total Monthly Revenue: ${total_monthly_revenue:,.2f}")
print(f"Total Variable Costs: ${total_monthly_cost:,.2f}")
print(f"Fixed Costs: ${total_fixed_costs:,.2f}")
print(f"Gross Profit: ${total_monthly_profit:,.2f}")
print(f"Net Profit (after fixed costs): ${total_monthly_profit - total_fixed_costs:,.2f}")
print(f"Overall Profit Margin: {overall_margin:.1f}%")

# --- Step 8: Visualizations ---
print("\n--- Generating Visualizations ---")
sns.set_style('whitegrid')

# 8a. Cost Breakdown Stacked Bar Chart
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(df_costs['coffee_name']))
width = 0.6

raw_mat = ax.bar(x, df_costs['raw_material_cost'], width, label='Raw Materials', color='#8B4513')
labor = ax.bar(x, df_costs['labor_cost'], width, bottom=df_costs['raw_material_cost'], 
               label='Labor', color='#CD853F')
overhead = ax.bar(x, df_costs['overhead_cost'], width, 
                  bottom=df_costs['raw_material_cost'] + df_costs['labor_cost'],
                  label='Overhead', color='#DEB887')

# Add selling price line
ax.plot(x, df_costs['selling_price'], 'ro-', linewidth=2, markersize=8, label='Selling Price')

ax.set_xlabel('Coffee Product', fontsize=12)
ax.set_ylabel('Cost / Price ($)', fontsize=12)
ax.set_title('Cost Breakdown vs Selling Price by Product', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(df_costs['coffee_name'], rotation=45, ha='right')
ax.legend()
plt.tight_layout()
plt.savefig('cost_breakdown_analysis.png', dpi=150)
print("Saved 'cost_breakdown_analysis.png'")

# 8b. Profit Margin Comparison
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['green' if x >= 50 else 'orange' if x >= 40 else 'red' 
          for x in df_costs['profit_margin_pct']]
bars = ax.bar(df_costs['coffee_name'], df_costs['profit_margin_pct'], color=colors)
ax.axhline(y=50, color='green', linestyle='--', label='Target Margin (50%)')
ax.axhline(y=40, color='orange', linestyle='--', label='Minimum Margin (40%)')
ax.set_xlabel('Coffee Product', fontsize=12)
ax.set_ylabel('Profit Margin (%)', fontsize=12)
ax.set_title('Profit Margin Analysis by Product', fontsize=14)
plt.xticks(rotation=45, ha='right')
ax.legend()
plt.tight_layout()
plt.savefig('profit_margin_analysis.png', dpi=150)
print("Saved 'profit_margin_analysis.png'")

# 8c. Monthly Profit Contribution
fig, ax = plt.subplots(figsize=(12, 6))
profit_sorted = df_costs.sort_values('monthly_profit', ascending=True)
ax.barh(profit_sorted['coffee_name'], profit_sorted['monthly_profit'], color='#2E8B57')
ax.set_xlabel('Monthly Profit ($)', fontsize=12)
ax.set_ylabel('Coffee Product', fontsize=12)
ax.set_title('Monthly Profit Contribution by Product', fontsize=14)
for i, v in enumerate(profit_sorted['monthly_profit']):
    ax.text(v + 20, i, f'${v:,.0f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('monthly_profit_contribution.png', dpi=150)
print("Saved 'monthly_profit_contribution.png'")

# 8d. Break-Even Analysis Chart
fig, ax = plt.subplots(figsize=(10, 6))
units_range = np.linspace(0, 10000, 100)
total_revenue = units_range * weighted_avg_price
# Variable cost per unit = selling price - contribution margin
weighted_avg_variable_cost = weighted_avg_price - weighted_avg_contribution
total_costs = total_fixed_costs + (units_range * weighted_avg_variable_cost)

ax.plot(units_range, total_revenue, 'b-', linewidth=2, label='Total Revenue')
ax.plot(units_range, total_costs, 'r-', linewidth=2, label='Total Costs')
ax.axvline(x=break_even_units, color='green', linestyle='--', 
           label=f'Break-Even ({break_even_units:,.0f} units)')
ax.fill_between(units_range, total_costs, total_revenue, 
                where=(total_revenue > total_costs), alpha=0.3, color='green', label='Profit Zone')
ax.fill_between(units_range, total_costs, total_revenue, 
                where=(total_revenue <= total_costs), alpha=0.3, color='red', label='Loss Zone')
ax.set_xlabel('Units Sold (drinks/month)', fontsize=12)
ax.set_ylabel('Dollars ($)', fontsize=12)
ax.set_title('Break-Even Analysis', fontsize=14)
ax.legend()
ax.set_xlim(0, 10000)
plt.tight_layout()
plt.savefig('break_even_analysis.png', dpi=150)
print("Saved 'break_even_analysis.png'")

# 8e. Cost Structure Pie Chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Average cost structure per drink (variable costs + allocated fixed costs)
cost_categories = ['Raw Materials', 'Labor', 'Overhead', 'Fixed Costs']
cost_values = [df_costs['raw_material_cost'].mean(), 
               df_costs['labor_cost'].mean(),
               df_costs['overhead_cost'].mean(),
               total_fixed_costs / total_sales_volume]

colors = ['#8B4513', '#CD853F', '#DEB887', '#F4A460']
axes[0].pie(cost_values, labels=cost_categories, autopct='%1.1f%%', colors=colors, startangle=90)
axes[0].set_title('Average Cost Structure per Drink', fontsize=12)

# Revenue distribution breakdown (Variable Costs + Fixed Costs + Net Profit = Total Revenue)
net_profit = total_monthly_revenue - total_monthly_cost - total_fixed_costs
revenue_cost = ['Variable Costs', 'Fixed Costs', 'Net Profit']
revenue_values = [total_monthly_cost, total_fixed_costs, net_profit]
colors2 = ['#FF6B6B', '#FFA500', '#4CAF50']
axes[1].pie(revenue_values, labels=revenue_cost, autopct='%1.1f%%', colors=colors2, startangle=90)
axes[1].set_title('Monthly Revenue Distribution', fontsize=12)

plt.tight_layout()
plt.savefig('cost_structure_overview.png', dpi=150)
print("Saved 'cost_structure_overview.png'")

# --- Step 9: Export Analysis Results ---
print("\n--- Exporting Analysis Results ---")

# Save detailed analysis to CSV
df_costs.to_csv('cost_pricing_analysis.csv', index=False)
print("Saved 'cost_pricing_analysis.csv'")

# Create summary report
summary_report = {
    'Metric': [
        'Total Monthly Revenue',
        'Total Variable Costs',
        'Total Fixed Costs',
        'Gross Profit',
        'Net Profit',
        'Overall Profit Margin',
        'Break-Even Units',
        'Break-Even Revenue',
        'Average Selling Price',
        'Average Cost per Drink',
        'Average Profit per Drink'
    ],
    'Value': [
        f"${total_monthly_revenue:,.2f}",
        f"${total_monthly_cost:,.2f}",
        f"${total_fixed_costs:,.2f}",
        f"${total_monthly_profit:,.2f}",
        f"${total_monthly_profit - total_fixed_costs:,.2f}",
        f"{overall_margin:.1f}%",
        f"{break_even_units:,.0f} drinks",
        f"${break_even_revenue:,.2f}",
        f"${weighted_avg_price:.2f}",
        f"${df_costs['total_cost'].mean():.2f}",
        f"${df_costs['profit_per_unit'].mean():.2f}"
    ]
}

df_summary = pd.DataFrame(summary_report)
df_summary.to_csv('financial_summary.csv', index=False)
print("Saved 'financial_summary.csv'")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print("\nGenerated Files:")
print("- cost_breakdown_analysis.png")
print("- profit_margin_analysis.png")
print("- monthly_profit_contribution.png")
print("- break_even_analysis.png")
print("- cost_structure_overview.png")
print("- cost_pricing_analysis.csv")
print("- financial_summary.csv")
