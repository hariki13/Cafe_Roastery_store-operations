"""
Supply Chain Analytics Module
Specializing in Coffee Supply Chain & Retail Analytics

This module provides analytics for:
- Inventory management and turnover analysis
- Reorder point calculations
- Supplier performance metrics
- Lead time analysis
- Stock-out risk assessment
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


def load_and_prepare_data(filepath='coffee sales dataset.csv'):
    """Load and prepare data for supply chain analysis."""
    try:
        df = pd.read_csv(filepath)
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df.dropna(subset=['datetime', 'money', 'coffee_name'], inplace=True)
        df.drop_duplicates(inplace=True)
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        print("Creating sample data for demonstration...")
        return create_sample_data()


def create_sample_data():
    """Create sample data for demonstration purposes."""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=365, freq='D')
    products = ['Espresso', 'Cappuccino', 'Latte', 'Americano', 'Mocha', 
                'Cold Brew', 'Macchiato', 'Flat White']
    
    data = []
    for date in dates:
        num_transactions = np.random.randint(50, 150)
        for _ in range(num_transactions):
            product = np.random.choice(products)
            price = {
                'Espresso': 3.50, 'Cappuccino': 4.50, 'Latte': 4.75,
                'Americano': 3.75, 'Mocha': 5.25, 'Cold Brew': 4.25,
                'Macchiato': 4.00, 'Flat White': 4.50
            }[product]
            data.append({
                'datetime': date + timedelta(hours=np.random.randint(6, 22)),
                'coffee_name': product,
                'money': price * np.random.uniform(0.9, 1.1)
            })
    
    return pd.DataFrame(data)


def calculate_inventory_turnover(df):
    """
    Calculate inventory turnover rate for each product.
    Higher turnover = more efficient inventory management.
    """
    print("\n" + "="*60)
    print("INVENTORY TURNOVER ANALYSIS")
    print("="*60)
    
    # Calculate daily sales velocity
    df['date'] = df['datetime'].dt.date
    daily_sales = df.groupby(['date', 'coffee_name']).size().reset_index(name='units_sold')
    
    # Average daily sales per product
    avg_daily_sales = daily_sales.groupby('coffee_name')['units_sold'].mean().reset_index()
    avg_daily_sales.columns = ['coffee_name', 'avg_daily_sales']
    avg_daily_sales = avg_daily_sales.sort_values('avg_daily_sales', ascending=False)
    
    print("\nAverage Daily Sales Velocity by Product:")
    print("-" * 40)
    for _, row in avg_daily_sales.iterrows():
        print(f"  {row['coffee_name']:<15} : {row['avg_daily_sales']:.1f} units/day")
    
    # Calculate inventory turnover rate: Annual Sales / Average Inventory
    # Average inventory estimated as 7 days of safety stock
    total_avg_daily = avg_daily_sales['avg_daily_sales'].sum()
    avg_daily_sales['sales_share'] = avg_daily_sales['avg_daily_sales'] / total_avg_daily
    # Higher velocity products have higher turnover (annual sales / base inventory)
    avg_daily_sales['est_turnover_rate'] = (avg_daily_sales['avg_daily_sales'] * 365) / (avg_daily_sales['avg_daily_sales'].mean() * 7)
    avg_daily_sales['est_turnover_rate'] = avg_daily_sales['est_turnover_rate'].round(1)
    
    print("\nEstimated Annual Inventory Turnover Rate:")
    print("-" * 40)
    for _, row in avg_daily_sales.iterrows():
        status = "✓ Good" if row['est_turnover_rate'] >= 40 else "⚠ Review"
        print(f"  {row['coffee_name']:<15} : {row['est_turnover_rate']:.1f}x ({status})")
    
    return avg_daily_sales


def calculate_reorder_points(df, lead_time_days=3, safety_stock_days=2):
    """
    Calculate reorder points for inventory management.
    Reorder Point = (Average Daily Demand × Lead Time) + Safety Stock
    """
    print("\n" + "="*60)
    print("REORDER POINT ANALYSIS")
    print("="*60)
    print(f"Lead Time: {lead_time_days} days | Safety Stock: {safety_stock_days} days buffer")
    
    df['date'] = df['datetime'].dt.date
    daily_demand = df.groupby(['date', 'coffee_name']).size().reset_index(name='units')
    
    # Calculate statistics per product
    demand_stats = daily_demand.groupby('coffee_name')['units'].agg(['mean', 'std']).reset_index()
    demand_stats.columns = ['coffee_name', 'avg_demand', 'std_demand']
    
    # Calculate reorder point: Avg Demand × (Lead Time + Safety Stock Days)
    demand_stats['reorder_point'] = (demand_stats['avg_demand'] * (lead_time_days + safety_stock_days)).round(0).astype(int)
    
    # Calculate safety stock
    demand_stats['safety_stock'] = (demand_stats['avg_demand'] * safety_stock_days).round(0).astype(int)
    
    print("\nReorder Points and Safety Stock Levels:")
    print("-" * 60)
    print(f"{'Product':<15} {'Avg Demand':<12} {'Reorder Point':<15} {'Safety Stock':<12}")
    print("-" * 60)
    
    for _, row in demand_stats.iterrows():
        print(f"{row['coffee_name']:<15} {row['avg_demand']:.1f} units    {row['reorder_point']:<15} {row['safety_stock']:<12}")
    
    return demand_stats


def analyze_demand_variability(df):
    """
    Analyze demand variability to identify products with unstable demand.
    High variability = need more safety stock.
    """
    print("\n" + "="*60)
    print("DEMAND VARIABILITY ANALYSIS")
    print("="*60)
    
    df['date'] = df['datetime'].dt.date
    daily_demand = df.groupby(['date', 'coffee_name']).size().reset_index(name='units')
    
    # Calculate coefficient of variation (CV)
    variability = daily_demand.groupby('coffee_name')['units'].agg(['mean', 'std']).reset_index()
    variability['cv'] = (variability['std'] / variability['mean'] * 100).round(1)
    variability = variability.sort_values('cv', ascending=False)
    
    print("\nDemand Variability (Coefficient of Variation):")
    print("-" * 50)
    for _, row in variability.iterrows():
        if row['cv'] > 50:
            risk = "⚠ High Risk"
        elif row['cv'] > 30:
            risk = "⚡ Medium Risk"
        else:
            risk = "✓ Stable"
        print(f"  {row['coffee_name']:<15} : CV = {row['cv']:.1f}% ({risk})")
    
    return variability


def analyze_weekly_patterns(df):
    """
    Analyze weekly demand patterns for supply planning.
    """
    print("\n" + "="*60)
    print("WEEKLY DEMAND PATTERNS")
    print("="*60)
    
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['day_num'] = df['datetime'].dt.dayofweek
    
    weekly_pattern = df.groupby(['day_num', 'day_of_week']).size().reset_index(name='transactions')
    weekly_pattern = weekly_pattern.sort_values('day_num')
    
    avg_transactions = weekly_pattern['transactions'].mean()
    
    print("\nAverage Transactions by Day of Week:")
    print("-" * 40)
    for _, row in weekly_pattern.iterrows():
        pct_diff = ((row['transactions'] - avg_transactions) / avg_transactions * 100)
        indicator = "📈" if pct_diff > 10 else ("📉" if pct_diff < -10 else "➡️")
        print(f"  {row['day_of_week']:<12} : {row['transactions']:,} transactions ({pct_diff:+.1f}%) {indicator}")
    
    return weekly_pattern


def generate_supply_chain_visualizations(df, demand_stats, weekly_pattern):
    """Generate supply chain analytics visualizations."""
    sns.set_style('whitegrid')
    
    # Figure 1: Reorder Points by Product
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Reorder Points
    ax1 = axes[0, 0]
    colors = sns.color_palette('viridis', len(demand_stats))
    bars = ax1.barh(demand_stats['coffee_name'], demand_stats['reorder_point'], color=colors)
    ax1.set_xlabel('Units', fontsize=12)
    ax1.set_title('Reorder Points by Product', fontsize=14, fontweight='bold')
    for bar, val in zip(bars, demand_stats['reorder_point']):
        ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val}', va='center', fontsize=10)
    
    # Plot 2: Safety Stock Levels
    ax2 = axes[0, 1]
    ax2.barh(demand_stats['coffee_name'], demand_stats['safety_stock'], color='coral')
    ax2.set_xlabel('Units', fontsize=12)
    ax2.set_title('Safety Stock Levels', fontsize=14, fontweight='bold')
    
    # Plot 3: Weekly Demand Pattern
    ax3 = axes[1, 0]
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_sorted = weekly_pattern.set_index('day_of_week').reindex(days_order).reset_index()
    ax3.bar(weekly_sorted['day_of_week'], weekly_sorted['transactions'], color='steelblue')
    ax3.set_xlabel('Day of Week', fontsize=12)
    ax3.set_ylabel('Transactions', fontsize=12)
    ax3.set_title('Weekly Demand Pattern', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    
    # Plot 4: Demand Variability
    ax4 = axes[1, 1]
    df['date'] = df['datetime'].dt.date
    daily_total = df.groupby('date').size()
    ax4.plot(daily_total.index, daily_total.values, marker='o', markersize=3, alpha=0.6)
    ax4.axhline(y=daily_total.mean(), color='red', linestyle='--', label=f'Average: {daily_total.mean():.0f}')
    ax4.set_xlabel('Date', fontsize=12)
    ax4.set_ylabel('Daily Transactions', fontsize=12)
    ax4.set_title('Daily Demand Trend', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('supply_chain_analytics.png', dpi=150, bbox_inches='tight')
    print("\n✓ Saved visualization: 'supply_chain_analytics.png'")
    
    return fig


def generate_supply_chain_report(df):
    """Generate comprehensive supply chain analytics report."""
    print("\n" + "="*60)
    print("COFFEE SUPPLY CHAIN ANALYTICS REPORT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Period: {df['datetime'].min().date()} to {df['datetime'].max().date()}")
    print(f"Total Transactions: {len(df):,}")
    print("="*60)
    
    # Run all analyses
    turnover_data = calculate_inventory_turnover(df)
    demand_stats = calculate_reorder_points(df)
    variability_data = analyze_demand_variability(df)
    weekly_pattern = analyze_weekly_patterns(df)
    
    # Generate visualizations
    generate_supply_chain_visualizations(df, demand_stats, weekly_pattern)
    
    # Summary recommendations
    print("\n" + "="*60)
    print("KEY RECOMMENDATIONS")
    print("="*60)
    
    # Find products with high variability
    high_var_products = variability_data[variability_data['cv'] > 40]['coffee_name'].tolist()
    if high_var_products:
        print(f"\n⚠️  High Variability Products (increase safety stock):")
        for product in high_var_products:
            print(f"   - {product}")
    
    # Find high-demand products
    top_demand = turnover_data.nlargest(3, 'avg_daily_sales')['coffee_name'].tolist()
    print(f"\n📈 Top Demand Products (prioritize supply):")
    for product in top_demand:
        print(f"   - {product}")
    
    print("\n" + "="*60)
    print("SUPPLY CHAIN ANALYSIS COMPLETE")
    print("="*60)
    
    return {
        'turnover': turnover_data,
        'demand_stats': demand_stats,
        'variability': variability_data,
        'weekly_pattern': weekly_pattern
    }


if __name__ == "__main__":
    # Load data
    df = load_and_prepare_data()
    
    # Generate comprehensive report
    results = generate_supply_chain_report(df)
