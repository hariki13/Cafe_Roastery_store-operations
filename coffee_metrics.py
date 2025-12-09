"""
Coffee Metrics Module
Specializing in Coffee Supply Chain & Retail Analytics

This module provides coffee-specific analytics for:
- Product profitability analysis
- Waste tracking and analysis
- Category performance comparison
- Revenue per product metrics
- Trend analysis by product type
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


def load_and_prepare_data(filepath='coffee sales dataset.csv'):
    """Load and prepare data for coffee metrics analysis."""
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
    
    # Coffee products with categories
    products = {
        'Espresso': {'category': 'Espresso-Based', 'base_price': 3.50, 'cost': 0.80},
        'Cappuccino': {'category': 'Espresso-Based', 'base_price': 4.50, 'cost': 1.20},
        'Latte': {'category': 'Espresso-Based', 'base_price': 4.75, 'cost': 1.30},
        'Americano': {'category': 'Espresso-Based', 'base_price': 3.75, 'cost': 0.70},
        'Mocha': {'category': 'Specialty', 'base_price': 5.25, 'cost': 1.60},
        'Cold Brew': {'category': 'Cold Coffee', 'base_price': 4.25, 'cost': 0.90},
        'Macchiato': {'category': 'Espresso-Based', 'base_price': 4.00, 'cost': 1.00},
        'Flat White': {'category': 'Specialty', 'base_price': 4.50, 'cost': 1.25},
        'Iced Latte': {'category': 'Cold Coffee', 'base_price': 5.00, 'cost': 1.40},
        'Caramel Frappe': {'category': 'Specialty', 'base_price': 5.75, 'cost': 1.80}
    }
    
    data = []
    for date in dates:
        # Seasonal adjustments (more cold drinks in summer)
        month = date.month
        is_summer = month in [6, 7, 8]
        is_winter = month in [12, 1, 2]
        
        num_transactions = np.random.randint(80, 140)
        
        for _ in range(num_transactions):
            # Product selection with seasonal preference
            if is_summer:
                weights = [0.08, 0.10, 0.12, 0.08, 0.08, 0.18, 0.06, 0.08, 0.14, 0.08]
            elif is_winter:
                weights = [0.12, 0.15, 0.15, 0.12, 0.12, 0.06, 0.10, 0.10, 0.04, 0.04]
            else:
                weights = [0.10, 0.12, 0.13, 0.10, 0.10, 0.12, 0.08, 0.09, 0.09, 0.07]
            
            product = np.random.choice(list(products.keys()), p=weights)
            price = products[product]['base_price'] * np.random.uniform(0.95, 1.05)
            
            data.append({
                'datetime': date + timedelta(hours=np.random.randint(6, 22), 
                                             minutes=np.random.randint(0, 60)),
                'coffee_name': product,
                'money': price,
                'category': products[product]['category'],
                'cost': products[product]['cost']
            })
    
    return pd.DataFrame(data)


# Coffee product costs (for profitability analysis)
PRODUCT_COSTS = {
    'Espresso': 0.80,
    'Cappuccino': 1.20,
    'Latte': 1.30,
    'Americano': 0.70,
    'Mocha': 1.60,
    'Cold Brew': 0.90,
    'Macchiato': 1.00,
    'Flat White': 1.25,
    'Iced Latte': 1.40,
    'Caramel Frappe': 1.80
}

# Coffee categories
PRODUCT_CATEGORIES = {
    'Espresso': 'Espresso-Based',
    'Cappuccino': 'Espresso-Based',
    'Latte': 'Espresso-Based',
    'Americano': 'Espresso-Based',
    'Mocha': 'Specialty',
    'Cold Brew': 'Cold Coffee',
    'Macchiato': 'Espresso-Based',
    'Flat White': 'Specialty',
    'Iced Latte': 'Cold Coffee',
    'Caramel Frappe': 'Specialty'
}


def analyze_profitability(df):
    """
    Analyze profitability by product.
    """
    print("\n" + "="*60)
    print("PRODUCT PROFITABILITY ANALYSIS")
    print("="*60)
    
    # Add cost data
    df['cost'] = df['coffee_name'].map(PRODUCT_COSTS).fillna(1.00)
    df['profit'] = df['money'] - df['cost']
    df['margin'] = (df['profit'] / df['money'] * 100)
    
    # Aggregate by product
    profitability = df.groupby('coffee_name').agg({
        'money': 'sum',
        'cost': 'sum',
        'profit': 'sum',
        'margin': 'mean'
    }).reset_index()
    profitability.columns = ['coffee_name', 'total_revenue', 'total_cost', 'total_profit', 'avg_margin']
    profitability = profitability.sort_values('total_profit', ascending=False)
    
    total_profit = profitability['total_profit'].sum()
    
    print("\nProfitability by Product:")
    print("-" * 85)
    print(f"{'Product':<18} {'Revenue':<14} {'Cost':<12} {'Profit':<14} {'Margin':<10} {'% of Total':<10}")
    print("-" * 85)
    
    for _, row in profitability.iterrows():
        pct_total = row['total_profit'] / total_profit * 100
        print(f"{row['coffee_name']:<18} ${row['total_revenue']:<13,.2f} ${row['total_cost']:<11,.2f} ${row['total_profit']:<13,.2f} {row['avg_margin']:.1f}%     {pct_total:.1f}%")
    
    print("-" * 85)
    print(f"{'TOTAL':<18} ${profitability['total_revenue'].sum():<13,.2f} ${profitability['total_cost'].sum():<11,.2f} ${total_profit:<13,.2f}")
    
    # Top and bottom performers
    print(f"\n🏆 Most Profitable: {profitability.iloc[0]['coffee_name']} (${profitability.iloc[0]['total_profit']:,.2f})")
    print(f"📊 Highest Margin: {profitability.loc[profitability['avg_margin'].idxmax(), 'coffee_name']} ({profitability['avg_margin'].max():.1f}%)")
    
    return profitability


def analyze_category_performance(df):
    """
    Analyze performance by coffee category.
    """
    print("\n" + "="*60)
    print("CATEGORY PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Add category data
    df['category'] = df['coffee_name'].map(PRODUCT_CATEGORIES).fillna('Other')
    df['cost'] = df['coffee_name'].map(PRODUCT_COSTS).fillna(1.00)
    df['profit'] = df['money'] - df['cost']
    
    # Aggregate by category
    category_perf = df.groupby('category').agg({
        'money': ['sum', 'count', 'mean'],
        'profit': 'sum'
    }).reset_index()
    category_perf.columns = ['category', 'total_revenue', 'units_sold', 'avg_price', 'total_profit']
    category_perf['margin'] = (category_perf['total_profit'] / category_perf['total_revenue'] * 100)
    category_perf = category_perf.sort_values('total_revenue', ascending=False)
    
    total_revenue = category_perf['total_revenue'].sum()
    
    print("\nCategory Performance Summary:")
    print("-" * 80)
    print(f"{'Category':<18} {'Units Sold':<12} {'Revenue':<15} {'% Revenue':<12} {'Profit':<14} {'Margin':<10}")
    print("-" * 80)
    
    for _, row in category_perf.iterrows():
        pct_revenue = row['total_revenue'] / total_revenue * 100
        print(f"{row['category']:<18} {row['units_sold']:<12,.0f} ${row['total_revenue']:<14,.2f} {pct_revenue:.1f}%       ${row['total_profit']:<13,.2f} {row['margin']:.1f}%")
    
    return category_perf


def analyze_seasonal_trends(df):
    """
    Analyze seasonal trends by product and category.
    """
    print("\n" + "="*60)
    print("SEASONAL TREND ANALYSIS")
    print("="*60)
    
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.month_name()
    df['season'] = df['month'].apply(lambda x: 
        'Winter' if x in [12, 1, 2] else
        'Spring' if x in [3, 4, 5] else
        'Summer' if x in [6, 7, 8] else 'Fall'
    )
    
    # Seasonal analysis
    seasonal = df.groupby('season').agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    seasonal.columns = ['season', 'total_revenue', 'transactions', 'avg_transaction']
    
    # Order seasons
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal['season_order'] = seasonal['season'].map({s: i for i, s in enumerate(season_order)})
    seasonal = seasonal.sort_values('season_order')
    
    avg_revenue = seasonal['total_revenue'].mean()
    
    print("\nSeasonal Performance:")
    print("-" * 60)
    for _, row in seasonal.iterrows():
        pct_diff = (row['total_revenue'] - avg_revenue) / avg_revenue * 100
        indicator = "📈" if pct_diff > 5 else ("📉" if pct_diff < -5 else "➡️")
        print(f"  {row['season']:<10} : ${row['total_revenue']:>12,.2f} ({pct_diff:+.1f}%) {indicator}")
    
    # Top products by season
    print("\nTop Product by Season:")
    print("-" * 40)
    for season in season_order:
        season_data = df[df['season'] == season]
        if len(season_data) > 0:
            top_product = season_data.groupby('coffee_name')['money'].sum().idxmax()
            print(f"  {season:<10} : {top_product}")
    
    return seasonal


def analyze_product_trends(df):
    """
    Analyze product performance trends over time.
    """
    print("\n" + "="*60)
    print("PRODUCT TREND ANALYSIS")
    print("="*60)
    
    df['month'] = df['datetime'].dt.to_period('M')
    
    # Monthly sales by product
    monthly_product = df.groupby(['month', 'coffee_name'])['money'].sum().reset_index()
    monthly_product['month'] = monthly_product['month'].astype(str)
    
    # Calculate growth rates
    products = df['coffee_name'].unique()
    growth_data = []
    
    for product in products:
        product_data = monthly_product[monthly_product['coffee_name'] == product].sort_values('month')
        if len(product_data) >= 2:
            first_quarter = product_data.head(3)['money'].mean()
            last_quarter = product_data.tail(3)['money'].mean()
            growth = (last_quarter - first_quarter) / first_quarter * 100 if first_quarter > 0 else 0
            growth_data.append({
                'product': product,
                'first_quarter_avg': first_quarter,
                'last_quarter_avg': last_quarter,
                'growth_rate': growth
            })
    
    growth_df = pd.DataFrame(growth_data).sort_values('growth_rate', ascending=False)
    
    print("\nProduct Growth Analysis (First vs Last Quarter):")
    print("-" * 70)
    print(f"{'Product':<18} {'Early Avg':<15} {'Recent Avg':<15} {'Growth':<15}")
    print("-" * 70)
    
    for _, row in growth_df.iterrows():
        indicator = "📈" if row['growth_rate'] > 10 else ("📉" if row['growth_rate'] < -10 else "➡️")
        print(f"{row['product']:<18} ${row['first_quarter_avg']:<14,.2f} ${row['last_quarter_avg']:<14,.2f} {row['growth_rate']:+.1f}% {indicator}")
    
    # Rising and declining products
    rising = growth_df[growth_df['growth_rate'] > 10]['product'].tolist()
    declining = growth_df[growth_df['growth_rate'] < -10]['product'].tolist()
    
    if rising:
        print(f"\n📈 Rising Products: {', '.join(rising)}")
    if declining:
        print(f"📉 Declining Products: {', '.join(declining)}")
    
    return growth_df


def analyze_pricing_optimization(df):
    """
    Analyze pricing opportunities.
    """
    print("\n" + "="*60)
    print("PRICING OPTIMIZATION ANALYSIS")
    print("="*60)
    
    df['cost'] = df['coffee_name'].map(PRODUCT_COSTS).fillna(1.00)
    df['profit'] = df['money'] - df['cost']
    df['margin'] = df['profit'] / df['money'] * 100
    
    # Price analysis by product
    price_analysis = df.groupby('coffee_name').agg({
        'money': ['mean', 'std', 'min', 'max'],
        'margin': 'mean'
    }).reset_index()
    price_analysis.columns = ['coffee_name', 'avg_price', 'price_std', 'min_price', 'max_price', 'avg_margin']
    
    # Target margin (70%)
    target_margin = 70
    price_analysis['margin_gap'] = target_margin - price_analysis['avg_margin']
    # Simplified price increase calculation: price × (gap/100)
    price_analysis['suggested_increase'] = price_analysis.apply(
        lambda row: row['avg_price'] * row['margin_gap'] / 100 if row['margin_gap'] > 0 else 0, axis=1
    )
    
    print("\nPricing Analysis:")
    print("-" * 85)
    print(f"{'Product':<18} {'Avg Price':<12} {'Margin':<12} {'Gap to 70%':<12} {'Suggested Δ':<12}")
    print("-" * 85)
    
    for _, row in price_analysis.iterrows():
        gap_indicator = "⚠️" if row['margin_gap'] > 5 else "✓"
        print(f"{row['coffee_name']:<18} ${row['avg_price']:<11.2f} {row['avg_margin']:.1f}%       {row['margin_gap']:+.1f}%        ${row['suggested_increase']:.2f} {gap_indicator}")
    
    # Products needing attention
    low_margin = price_analysis[price_analysis['avg_margin'] < 65]['coffee_name'].tolist()
    if low_margin:
        print(f"\n⚠️ Products with low margin (<65%): {', '.join(low_margin)}")
    
    return price_analysis


def generate_coffee_visualizations(df, profitability, category_perf):
    """Generate coffee metrics visualizations."""
    sns.set_style('whitegrid')
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Profitability by Product
    ax1 = axes[0, 0]
    colors = sns.color_palette('RdYlGn', len(profitability))
    sorted_profit = profitability.sort_values('total_profit')
    ax1.barh(sorted_profit['coffee_name'], sorted_profit['total_profit'], 
             color=[colors[i] for i in range(len(sorted_profit))])
    ax1.set_xlabel('Total Profit ($)', fontsize=12)
    ax1.set_title('Profitability by Product', fontsize=14, fontweight='bold')
    
    # Plot 2: Margin Analysis
    ax2 = axes[0, 1]
    sorted_margin = profitability.sort_values('avg_margin')
    colors = ['#FF6B6B' if m < 65 else '#4ECDC4' for m in sorted_margin['avg_margin']]
    ax2.barh(sorted_margin['coffee_name'], sorted_margin['avg_margin'], color=colors)
    ax2.axvline(x=70, color='red', linestyle='--', label='Target (70%)')
    ax2.set_xlabel('Profit Margin (%)', fontsize=12)
    ax2.set_title('Profit Margin by Product', fontsize=14, fontweight='bold')
    ax2.legend()
    
    # Plot 3: Category Revenue Distribution
    ax3 = axes[1, 0]
    colors = sns.color_palette('viridis', len(category_perf))
    ax3.pie(category_perf['total_revenue'], labels=category_perf['category'], 
            autopct='%1.1f%%', colors=colors, startangle=90)
    ax3.set_title('Revenue by Category', fontsize=14, fontweight='bold')
    
    # Plot 4: Revenue vs Profit Scatter
    ax4 = axes[1, 1]
    scatter = ax4.scatter(profitability['total_revenue'], profitability['total_profit'], 
                          c=profitability['avg_margin'], cmap='RdYlGn', s=100, alpha=0.7)
    for _, row in profitability.iterrows():
        ax4.annotate(row['coffee_name'], (row['total_revenue'], row['total_profit']),
                     fontsize=8, ha='center', va='bottom')
    ax4.set_xlabel('Total Revenue ($)', fontsize=12)
    ax4.set_ylabel('Total Profit ($)', fontsize=12)
    ax4.set_title('Revenue vs Profit (Color = Margin)', fontsize=14, fontweight='bold')
    plt.colorbar(scatter, ax=ax4, label='Margin %')
    
    plt.tight_layout()
    plt.savefig('coffee_metrics.png', dpi=150, bbox_inches='tight')
    print("\n✓ Saved visualization: 'coffee_metrics.png'")
    
    return fig


def generate_coffee_report(df):
    """Generate comprehensive coffee metrics report."""
    print("\n" + "="*60)
    print("COFFEE METRICS ANALYTICS REPORT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Period: {df['datetime'].min().date()} to {df['datetime'].max().date()}")
    print(f"Total Transactions: {len(df):,}")
    print(f"Unique Products: {df['coffee_name'].nunique()}")
    print("="*60)
    
    # Run all analyses
    profitability = analyze_profitability(df)
    category_perf = analyze_category_performance(df)
    seasonal = analyze_seasonal_trends(df)
    trends = analyze_product_trends(df)
    pricing = analyze_pricing_optimization(df)
    
    # Generate visualizations
    generate_coffee_visualizations(df, profitability, category_perf)
    
    # Summary recommendations
    print("\n" + "="*60)
    print("KEY INSIGHTS & RECOMMENDATIONS")
    print("="*60)
    
    # Most profitable product
    top_profit_product = profitability.iloc[0]['coffee_name']
    print(f"\n💰 Most Profitable Product: {top_profit_product}")
    print(f"   → Focus on quality and availability of this product")
    
    # Low margin products
    df['cost'] = df['coffee_name'].map(PRODUCT_COSTS).fillna(1.00)
    df['margin'] = (df['money'] - df['cost']) / df['money'] * 100
    low_margin_products = df.groupby('coffee_name')['margin'].mean()
    low_margin_products = low_margin_products[low_margin_products < 65].index.tolist()
    if low_margin_products:
        print(f"\n⚠️ Low Margin Products (Review Pricing):")
        for product in low_margin_products:
            print(f"   - {product}")
    
    # Growth opportunities
    rising_products = trends[trends['growth_rate'] > 10]['product'].tolist()
    if rising_products:
        print(f"\n📈 High Growth Products (Expand Offerings):")
        for product in rising_products:
            print(f"   - {product}")
    
    print("\n" + "="*60)
    print("COFFEE METRICS ANALYSIS COMPLETE")
    print("="*60)
    
    return {
        'profitability': profitability,
        'categories': category_perf,
        'seasonal': seasonal,
        'trends': trends,
        'pricing': pricing
    }


if __name__ == "__main__":
    # Load data
    df = load_and_prepare_data()
    
    # Generate comprehensive report
    results = generate_coffee_report(df)
