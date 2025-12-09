"""
Retail Analytics Module
Specializing in Coffee Supply Chain & Retail Analytics

This module provides analytics for:
- Peak hours analysis
- Customer purchase patterns
- Sales forecasting
- Seasonal trend detection
- Payment method analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


def load_and_prepare_data(filepath='coffee sales dataset.csv'):
    """Load and prepare data for retail analysis."""
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
    payment_types = ['cash', 'card']
    
    data = []
    for date in dates:
        # More transactions on weekends
        base_transactions = 100 if date.dayofweek < 5 else 130
        num_transactions = np.random.randint(int(base_transactions*0.7), int(base_transactions*1.3))
        
        for _ in range(num_transactions):
            # Peak hours: 7-9 AM and 2-4 PM
            hour = np.random.choice(
                range(6, 22),
                p=create_hour_weights()
            )
            product = np.random.choice(products)
            price = {
                'Espresso': 3.50, 'Cappuccino': 4.50, 'Latte': 4.75,
                'Americano': 3.75, 'Mocha': 5.25, 'Cold Brew': 4.25,
                'Macchiato': 4.00, 'Flat White': 4.50
            }[product]
            
            data.append({
                'datetime': date + timedelta(hours=int(hour), minutes=int(np.random.randint(0, 60))),
                'coffee_name': product,
                'money': price * np.random.uniform(0.9, 1.1),
                'cash_type': np.random.choice(payment_types, p=[0.3, 0.7])
            })
    
    return pd.DataFrame(data)


def create_hour_weights():
    """Create realistic hour weights for coffee shop traffic."""
    # Hours 6-21 (6 AM to 9 PM)
    weights = [
        0.02,  # 6 AM
        0.08,  # 7 AM - morning rush starts
        0.12,  # 8 AM - peak morning
        0.10,  # 9 AM - morning rush ends
        0.07,  # 10 AM
        0.06,  # 11 AM
        0.07,  # 12 PM - lunch
        0.06,  # 1 PM
        0.08,  # 2 PM - afternoon rush
        0.09,  # 3 PM - afternoon peak
        0.07,  # 4 PM
        0.05,  # 5 PM
        0.05,  # 6 PM
        0.04,  # 7 PM
        0.03,  # 8 PM
        0.01   # 9 PM
    ]
    return weights


def analyze_peak_hours(df):
    """
    Analyze transaction patterns by hour to identify peak business hours.
    """
    print("\n" + "="*60)
    print("PEAK HOURS ANALYSIS")
    print("="*60)
    
    df['hour'] = df['datetime'].dt.hour
    hourly_analysis = df.groupby('hour').agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    hourly_analysis.columns = ['hour', 'total_revenue', 'transactions', 'avg_transaction']
    
    avg_transactions = hourly_analysis['transactions'].mean()
    
    print("\nHourly Transaction Analysis:")
    print("-" * 70)
    print(f"{'Hour':<8} {'Transactions':<15} {'Revenue':<15} {'Avg Transaction':<15} {'Status':<10}")
    print("-" * 70)
    
    for _, row in hourly_analysis.iterrows():
        hour_str = f"{int(row['hour']):02d}:00"
        pct_diff = (row['transactions'] - avg_transactions) / avg_transactions * 100
        
        if pct_diff > 30:
            status = "🔥 PEAK"
        elif pct_diff > 10:
            status = "📈 High"
        elif pct_diff < -30:
            status = "📉 Low"
        else:
            status = "➡️ Normal"
        
        print(f"{hour_str:<8} {row['transactions']:<15,.0f} ${row['total_revenue']:<14,.2f} ${row['avg_transaction']:<14.2f} {status}")
    
    # Identify peak hours
    peak_hours = hourly_analysis[hourly_analysis['transactions'] > avg_transactions * 1.2]['hour'].tolist()
    print(f"\n🔥 Peak Hours: {', '.join([f'{h:02d}:00' for h in peak_hours])}")
    
    return hourly_analysis


def analyze_daily_patterns(df):
    """
    Analyze sales patterns by day of week.
    """
    print("\n" + "="*60)
    print("DAILY SALES PATTERNS")
    print("="*60)
    
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['day_num'] = df['datetime'].dt.dayofweek
    
    daily_analysis = df.groupby(['day_num', 'day_of_week']).agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    daily_analysis.columns = ['day_num', 'day_of_week', 'total_revenue', 'transactions', 'avg_transaction']
    daily_analysis = daily_analysis.sort_values('day_num')
    
    total_revenue = daily_analysis['total_revenue'].sum()
    
    print("\nDaily Performance Analysis:")
    print("-" * 70)
    print(f"{'Day':<12} {'Transactions':<15} {'Revenue':<15} {'% of Total':<12} {'Avg Trans':<12}")
    print("-" * 70)
    
    for _, row in daily_analysis.iterrows():
        pct_total = row['total_revenue'] / total_revenue * 100
        print(f"{row['day_of_week']:<12} {row['transactions']:<15,.0f} ${row['total_revenue']:<14,.2f} {pct_total:.1f}%        ${row['avg_transaction']:.2f}")
    
    # Best and worst days
    best_day = daily_analysis.loc[daily_analysis['total_revenue'].idxmax(), 'day_of_week']
    worst_day = daily_analysis.loc[daily_analysis['total_revenue'].idxmin(), 'day_of_week']
    
    print(f"\n📈 Best Day: {best_day}")
    print(f"📉 Slowest Day: {worst_day}")
    
    return daily_analysis


def analyze_monthly_trends(df):
    """
    Analyze monthly sales trends for seasonal patterns.
    """
    print("\n" + "="*60)
    print("MONTHLY SALES TRENDS")
    print("="*60)
    
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.month_name()
    
    monthly_analysis = df.groupby(['month', 'month_name']).agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    monthly_analysis.columns = ['month', 'month_name', 'total_revenue', 'transactions', 'avg_transaction']
    monthly_analysis = monthly_analysis.sort_values('month')
    
    avg_revenue = monthly_analysis['total_revenue'].mean()
    
    print("\nMonthly Performance Analysis:")
    print("-" * 60)
    
    for _, row in monthly_analysis.iterrows():
        pct_diff = (row['total_revenue'] - avg_revenue) / avg_revenue * 100
        indicator = "📈" if pct_diff > 10 else ("📉" if pct_diff < -10 else "➡️")
        print(f"{row['month_name']:<12} : ${row['total_revenue']:>12,.2f} ({pct_diff:+.1f}%) {indicator}")
    
    return monthly_analysis


def analyze_product_performance(df):
    """
    Analyze product performance and popularity.
    """
    print("\n" + "="*60)
    print("PRODUCT PERFORMANCE ANALYSIS")
    print("="*60)
    
    product_analysis = df.groupby('coffee_name').agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    product_analysis.columns = ['coffee_name', 'total_revenue', 'units_sold', 'avg_price']
    product_analysis = product_analysis.sort_values('total_revenue', ascending=False)
    
    total_revenue = product_analysis['total_revenue'].sum()
    total_units = product_analysis['units_sold'].sum()
    
    print("\nProduct Performance Summary:")
    print("-" * 80)
    print(f"{'Product':<15} {'Units Sold':<12} {'Revenue':<15} {'% Revenue':<12} {'Avg Price':<12}")
    print("-" * 80)
    
    for _, row in product_analysis.iterrows():
        pct_revenue = row['total_revenue'] / total_revenue * 100
        print(f"{row['coffee_name']:<15} {row['units_sold']:<12,.0f} ${row['total_revenue']:<14,.2f} {pct_revenue:.1f}%       ${row['avg_price']:.2f}")
    
    # Top and bottom performers
    print(f"\n🏆 Top Seller: {product_analysis.iloc[0]['coffee_name']} (${product_analysis.iloc[0]['total_revenue']:,.2f})")
    print(f"📊 Top by Volume: {product_analysis.sort_values('units_sold', ascending=False).iloc[0]['coffee_name']} ({product_analysis.sort_values('units_sold', ascending=False).iloc[0]['units_sold']:,.0f} units)")
    
    return product_analysis


def analyze_payment_methods(df):
    """
    Analyze payment method preferences.
    """
    print("\n" + "="*60)
    print("PAYMENT METHOD ANALYSIS")
    print("="*60)
    
    if 'cash_type' not in df.columns:
        print("⚠️ Payment method data not available in dataset")
        return None
    
    payment_analysis = df.groupby('cash_type').agg({
        'money': ['sum', 'count', 'mean']
    }).reset_index()
    payment_analysis.columns = ['payment_method', 'total_revenue', 'transactions', 'avg_transaction']
    
    total_transactions = payment_analysis['transactions'].sum()
    
    print("\nPayment Method Distribution:")
    print("-" * 60)
    
    for _, row in payment_analysis.iterrows():
        pct = row['transactions'] / total_transactions * 100
        print(f"{row['payment_method'].upper():<10} : {row['transactions']:>10,} transactions ({pct:.1f}%) | ${row['total_revenue']:>12,.2f}")
    
    return payment_analysis


def simple_sales_forecast(df, forecast_days=30):
    """
    Generate simple sales forecast based on historical trends.
    """
    print("\n" + "="*60)
    print("SALES FORECAST (Next 30 Days)")
    print("="*60)
    
    df['date'] = df['datetime'].dt.date
    daily_sales = df.groupby('date')['money'].sum().reset_index()
    daily_sales['date'] = pd.to_datetime(daily_sales['date'])
    
    # Calculate moving averages
    daily_sales['ma_7'] = daily_sales['money'].rolling(window=7).mean()
    daily_sales['ma_30'] = daily_sales['money'].rolling(window=30).mean()
    
    # Simple forecast using recent trend
    recent_avg = daily_sales['money'].tail(30).mean()
    recent_trend = (daily_sales['money'].tail(7).mean() - daily_sales['money'].tail(30).mean()) / daily_sales['money'].tail(30).mean()
    
    print(f"\nHistorical Analysis:")
    print(f"  - Average Daily Revenue (Last 30 days): ${recent_avg:,.2f}")
    print(f"  - Recent Trend: {recent_trend*100:+.1f}%")
    
    # Generate forecast
    last_date = daily_sales['date'].max()
    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_days)
    
    forecasted_revenue = []
    base = recent_avg
    for i, date in enumerate(forecast_dates):
        # Apply trend and day-of-week seasonality
        day_factor = 1.1 if date.dayofweek >= 5 else 1.0  # Higher on weekends
        forecast = base * day_factor * (1 + recent_trend * (i / forecast_days))
        forecasted_revenue.append(forecast)
    
    total_forecast = sum(forecasted_revenue)
    
    print(f"\n📊 30-Day Revenue Forecast: ${total_forecast:,.2f}")
    print(f"   Daily Average Forecast: ${total_forecast/30:,.2f}")
    
    return {
        'forecast_dates': forecast_dates,
        'forecast_values': forecasted_revenue,
        'historical': daily_sales
    }


def generate_retail_visualizations(df, hourly_data, daily_data, product_data):
    """Generate retail analytics visualizations."""
    sns.set_style('whitegrid')
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Hourly Traffic
    ax1 = axes[0, 0]
    colors = ['#FF6B6B' if t > hourly_data['transactions'].mean() * 1.2 else '#4ECDC4' 
              for t in hourly_data['transactions']]
    ax1.bar([f"{int(h):02d}:00" for h in hourly_data['hour']], 
            hourly_data['transactions'], color=colors)
    ax1.axhline(y=hourly_data['transactions'].mean(), color='red', linestyle='--', 
                label=f'Average: {hourly_data["transactions"].mean():.0f}')
    ax1.set_xlabel('Hour', fontsize=12)
    ax1.set_ylabel('Transactions', fontsize=12)
    ax1.set_title('Hourly Transaction Volume', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()
    
    # Plot 2: Daily Revenue
    ax2 = axes[0, 1]
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_sorted = daily_data.set_index('day_of_week').reindex(days_order).reset_index()
    colors = sns.color_palette('YlOrRd', len(daily_sorted))
    sorted_indices = daily_sorted['total_revenue'].argsort()
    bar_colors = [colors[list(sorted_indices).index(i)] for i in range(len(daily_sorted))]
    ax2.bar(daily_sorted['day_of_week'], daily_sorted['total_revenue'], color=bar_colors)
    ax2.set_xlabel('Day of Week', fontsize=12)
    ax2.set_ylabel('Revenue ($)', fontsize=12)
    ax2.set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Plot 3: Product Performance
    ax3 = axes[1, 0]
    top_products = product_data.nlargest(8, 'total_revenue')
    ax3.barh(top_products['coffee_name'], top_products['total_revenue'], 
             color=sns.color_palette('viridis', len(top_products)))
    ax3.set_xlabel('Revenue ($)', fontsize=12)
    ax3.set_title('Product Revenue Performance', fontsize=14, fontweight='bold')
    
    # Plot 4: Revenue Trend
    ax4 = axes[1, 1]
    df['date'] = df['datetime'].dt.date
    daily_revenue = df.groupby('date')['money'].sum()
    ax4.plot(daily_revenue.index, daily_revenue.values, linewidth=1, alpha=0.7)
    ax4.plot(daily_revenue.rolling(7).mean().index, daily_revenue.rolling(7).mean().values, 
             color='red', linewidth=2, label='7-day MA')
    ax4.set_xlabel('Date', fontsize=12)
    ax4.set_ylabel('Daily Revenue ($)', fontsize=12)
    ax4.set_title('Daily Revenue Trend', fontsize=14, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('retail_analytics.png', dpi=150, bbox_inches='tight')
    print("\n✓ Saved visualization: 'retail_analytics.png'")
    
    return fig


def generate_retail_report(df):
    """Generate comprehensive retail analytics report."""
    print("\n" + "="*60)
    print("COFFEE RETAIL ANALYTICS REPORT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Period: {df['datetime'].min().date()} to {df['datetime'].max().date()}")
    print(f"Total Transactions: {len(df):,}")
    print(f"Total Revenue: ${df['money'].sum():,.2f}")
    print("="*60)
    
    # Run all analyses
    hourly_data = analyze_peak_hours(df)
    daily_data = analyze_daily_patterns(df)
    monthly_data = analyze_monthly_trends(df)
    product_data = analyze_product_performance(df)
    payment_data = analyze_payment_methods(df)
    forecast_data = simple_sales_forecast(df)
    
    # Generate visualizations
    generate_retail_visualizations(df, hourly_data, daily_data, product_data)
    
    # Summary and recommendations
    print("\n" + "="*60)
    print("KEY INSIGHTS & RECOMMENDATIONS")
    print("="*60)
    
    # Peak hours recommendation
    peak_hours = hourly_data[hourly_data['transactions'] > hourly_data['transactions'].mean() * 1.2]['hour'].tolist()
    print(f"\n⏰ Staff Scheduling: Increase staff during peak hours: {', '.join([f'{h:02d}:00' for h in peak_hours])}")
    
    # Best day recommendation
    best_day = daily_data.loc[daily_data['total_revenue'].idxmax(), 'day_of_week']
    print(f"📅 Best Performing Day: {best_day} - consider promotions on slower days")
    
    # Top product insight
    top_product = product_data.iloc[0]['coffee_name']
    print(f"☕ Best Seller: {top_product} - ensure consistent quality and supply")
    
    print("\n" + "="*60)
    print("RETAIL ANALYTICS COMPLETE")
    print("="*60)
    
    return {
        'hourly': hourly_data,
        'daily': daily_data,
        'monthly': monthly_data,
        'products': product_data,
        'payments': payment_data,
        'forecast': forecast_data
    }


if __name__ == "__main__":
    # Load data
    df = load_and_prepare_data()
    
    # Generate comprehensive report
    results = generate_retail_report(df)
