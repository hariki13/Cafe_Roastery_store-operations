# --- Coffee Brand Operations & Inventory Analytics Module ---
"""
Enhanced analytics module for helping coffee brands optimize operations and inventory.
Provides comprehensive data analysis, trend detection, and actionable insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import warnings

warnings.filterwarnings('ignore')


class CoffeeAnalytics:
    """Main analytics class for coffee shop operations and inventory optimization."""
    
    def __init__(self, filepath='coffee sales dataset.csv'):
        """Initialize with data file path."""
        self.filepath = filepath
        self.df = None
        self.cleaned = False
        
    def load_data(self):
        """Load data from CSV file."""
        self.df = pd.read_csv(self.filepath)
        print(f"Loaded {len(self.df)} records from {self.filepath}")
        return self
    
    def get_data_info(self):
        """Return basic information about the dataset."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict()
        }
    
    def clean_data(self):
        """
        Clean and prepare the data for analysis.
        - Converts datetime column to proper datetime type
        - Removes rows with missing critical values
        - Removes duplicate rows
        - Extracts time-based features for analysis
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        initial_rows = len(self.df)
        
        # Convert datetime column
        self.df['datetime'] = pd.to_datetime(self.df['datetime'], errors='coerce')
        
        # Remove rows with missing critical values
        self.df.dropna(subset=['datetime', 'money', 'coffee_name'], inplace=True)
        
        # Remove duplicates
        self.df.drop_duplicates(inplace=True)
        
        # Extract time-based features for enhanced analysis
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.dayofweek
        self.df['day_name'] = self.df['datetime'].dt.day_name()
        self.df['month'] = self.df['datetime'].dt.month
        self.df['month_name'] = self.df['datetime'].dt.month_name()
        self.df['week'] = self.df['datetime'].dt.isocalendar().week
        self.df['date'] = self.df['datetime'].dt.date
        
        removed_rows = initial_rows - len(self.df)
        print(f"Data cleaning complete. Removed {removed_rows} rows.")
        print(f"Clean dataset contains {len(self.df)} records.")
        
        self.cleaned = True
        return self
    
    def get_descriptive_stats(self):
        """Calculate basic descriptive statistics for sales."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        stats = {
            'total_sales': self.df['money'].sum(),
            'average_transaction': self.df['money'].mean(),
            'median_transaction': self.df['money'].median(),
            'max_transaction': self.df['money'].max(),
            'min_transaction': self.df['money'].min(),
            'std_deviation': self.df['money'].std(),
            'total_transactions': len(self.df),
            'unique_products': self.df['coffee_name'].nunique()
        }
        return stats
    
    # --- PRODUCT ANALYSIS ---
    
    def analyze_products(self, top_n=5):
        """
        Analyze product performance.
        Returns top N products by sales and items sold.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        product_analysis = self.df.groupby('coffee_name')['money'].agg([
            ('total_sales', 'sum'),
            ('items_sold', 'count'),
            ('avg_price', 'mean')
        ]).reset_index()
        
        # Calculate percentage of total sales
        total = product_analysis['total_sales'].sum()
        product_analysis['sales_percentage'] = (product_analysis['total_sales'] / total * 100).round(2)
        
        top_by_sales = product_analysis.sort_values(by='total_sales', ascending=False).head(top_n)
        top_by_items = product_analysis.sort_values(by='items_sold', ascending=False).head(top_n)
        
        return {
            'full_analysis': product_analysis,
            'top_by_sales': top_by_sales,
            'top_by_items_sold': top_by_items
        }
    
    # --- TIME-BASED ANALYSIS ---
    
    def analyze_hourly_sales(self):
        """
        Analyze sales by hour to identify peak hours.
        Critical for staff scheduling and inventory preparation.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        hourly_stats = self.df.groupby('hour').agg({
            'money': ['sum', 'mean', 'count']
        }).round(2)
        hourly_stats.columns = ['total_sales', 'avg_transaction', 'transaction_count']
        hourly_stats = hourly_stats.reset_index()
        
        # Identify peak hours (top 3 by sales)
        peak_hours = hourly_stats.nlargest(3, 'total_sales')['hour'].tolist()
        slow_hours = hourly_stats.nsmallest(3, 'total_sales')['hour'].tolist()
        
        return {
            'hourly_stats': hourly_stats,
            'peak_hours': peak_hours,
            'slow_hours': slow_hours,
            'recommendation': f"Peak hours: {peak_hours}. Consider extra staffing and inventory during these times."
        }
    
    def analyze_daily_sales(self):
        """
        Analyze sales by day of week.
        Helps identify busy days for operations planning.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        daily_stats = self.df.groupby(['day_of_week', 'day_name']).agg({
            'money': ['sum', 'mean', 'count']
        }).round(2)
        daily_stats.columns = ['total_sales', 'avg_transaction', 'transaction_count']
        daily_stats = daily_stats.reset_index()
        daily_stats = daily_stats.sort_values('day_of_week')
        
        busiest_day = daily_stats.loc[daily_stats['total_sales'].idxmax(), 'day_name']
        slowest_day = daily_stats.loc[daily_stats['total_sales'].idxmin(), 'day_name']
        
        return {
            'daily_stats': daily_stats,
            'busiest_day': busiest_day,
            'slowest_day': slowest_day
        }
    
    def analyze_weekly_trends(self):
        """Analyze sales trends by week for longer-term patterns."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        weekly_sales = self.df.groupby('week').agg({
            'money': ['sum', 'count'],
            'datetime': 'min'
        }).reset_index()
        weekly_sales.columns = ['week', 'total_sales', 'transactions', 'week_start']
        
        # Calculate week-over-week growth
        weekly_sales['wow_growth'] = weekly_sales['total_sales'].pct_change() * 100
        
        return weekly_sales
    
    def analyze_monthly_trends(self):
        """Analyze sales trends by month."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        monthly_sales = self.df.groupby(['month', 'month_name']).agg({
            'money': ['sum', 'mean', 'count']
        }).reset_index()
        monthly_sales.columns = ['month', 'month_name', 'total_sales', 'avg_transaction', 'transactions']
        monthly_sales = monthly_sales.sort_values('month')
        
        # Calculate month-over-month growth
        monthly_sales['mom_growth'] = monthly_sales['total_sales'].pct_change() * 100
        
        return monthly_sales
    
    def get_daily_sales_trend(self):
        """Get daily sales for trend visualization."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        daily_sales = self.df.set_index('datetime').resample('D')['money'].agg(['sum', 'count'])
        daily_sales.columns = ['total_sales', 'transactions']
        
        # Add 7-day moving average for trend smoothing
        daily_sales['moving_avg_7d'] = daily_sales['total_sales'].rolling(window=7, min_periods=1).mean()
        
        return daily_sales
    
    # --- INVENTORY OPTIMIZATION ---
    
    def get_inventory_recommendations(self):
        """
        Generate inventory optimization recommendations based on sales data.
        Helps coffee brands maintain optimal stock levels.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        # Product velocity analysis
        product_stats = self.df.groupby('coffee_name').agg({
            'money': ['sum', 'count', 'mean'],
            'datetime': ['min', 'max']
        }).reset_index()
        product_stats.columns = ['product', 'total_sales', 'units_sold', 'avg_price', 
                                  'first_sale', 'last_sale']
        
        # Calculate days in range and daily velocity
        product_stats['days_range'] = (product_stats['last_sale'] - product_stats['first_sale']).dt.days + 1
        product_stats['daily_velocity'] = product_stats['units_sold'] / product_stats['days_range']
        
        # Classify products by velocity
        velocity_75th = product_stats['daily_velocity'].quantile(0.75)
        velocity_25th = product_stats['daily_velocity'].quantile(0.25)
        
        def classify_velocity(vel):
            if vel >= velocity_75th:
                return 'High'
            elif vel >= velocity_25th:
                return 'Medium'
            return 'Low'
        
        product_stats['velocity_class'] = product_stats['daily_velocity'].apply(classify_velocity)
        
        # Generate recommendations
        high_velocity = product_stats[product_stats['velocity_class'] == 'High']['product'].tolist()
        low_velocity = product_stats[product_stats['velocity_class'] == 'Low']['product'].tolist()
        
        recommendations = {
            'product_velocity': product_stats[['product', 'units_sold', 'daily_velocity', 'velocity_class']],
            'high_velocity_products': high_velocity,
            'low_velocity_products': low_velocity,
            'restock_priority': high_velocity[:5],
            'review_for_discontinuation': low_velocity[:3],
            'insights': []
        }
        
        # Add actionable insights
        if high_velocity:
            recommendations['insights'].append(
                f"High-demand products ({', '.join(high_velocity[:3])}): Ensure adequate stock levels and consider bulk purchasing for cost savings."
            )
        if low_velocity:
            recommendations['insights'].append(
                f"Low-demand products ({', '.join(low_velocity[:3])}): Review pricing strategy, consider promotions, or phase out."
            )
        
        return recommendations
    
    def get_peak_demand_forecast(self):
        """
        Analyze demand patterns to help with inventory forecasting.
        Returns peak demand times and recommended stock levels.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        # Hourly demand by product
        hourly_product_demand = self.df.groupby(['hour', 'coffee_name']).size().reset_index(name='count')
        
        # Find peak demand hour for each product
        peak_hours_by_product = hourly_product_demand.loc[
            hourly_product_demand.groupby('coffee_name')['count'].idxmax()
        ][['coffee_name', 'hour', 'count']]
        peak_hours_by_product.columns = ['product', 'peak_hour', 'peak_demand']
        
        # Daily demand patterns
        daily_product_demand = self.df.groupby(['day_name', 'coffee_name']).size().reset_index(name='count')
        
        return {
            'hourly_product_demand': hourly_product_demand,
            'peak_hours_by_product': peak_hours_by_product,
            'daily_product_demand': daily_product_demand
        }
    
    # --- CUSTOMER INSIGHTS ---
    
    def analyze_transaction_segments(self):
        """
        Segment transactions by value to understand customer behavior.
        Helps with pricing strategies and promotions.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        # Define transaction value segments
        bins = [0, 3, 5, 10, float('inf')]
        labels = ['Low (<$3)', 'Medium ($3-5)', 'High ($5-10)', 'Premium (>$10)']
        
        self.df['transaction_segment'] = pd.cut(self.df['money'], bins=bins, labels=labels)
        
        # observed=False ensures all segment categories are included even if empty
        segment_analysis = self.df.groupby('transaction_segment', observed=False).agg({
            'money': ['sum', 'count', 'mean']
        }).reset_index()
        segment_analysis.columns = ['segment', 'total_revenue', 'transaction_count', 'avg_value']
        
        # Calculate percentages
        total_revenue = segment_analysis['total_revenue'].sum()
        segment_analysis['revenue_share'] = (segment_analysis['total_revenue'] / total_revenue * 100).round(2)
        
        return segment_analysis
    
    def get_payment_analysis(self):
        """
        Analyze payment methods if available in data.
        Returns payment method distribution.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        if 'cash_type' not in self.df.columns:
            return {'message': 'Payment method data not available in dataset'}
        
        payment_stats = self.df.groupby('cash_type').agg({
            'money': ['sum', 'count', 'mean']
        }).reset_index()
        payment_stats.columns = ['payment_method', 'total_sales', 'transactions', 'avg_transaction']
        
        return payment_stats
    
    # --- VISUALIZATION ---
    
    def plot_top_products(self, top_n=5, save=True, show=False):
        """Create visualization of top products by sales."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        product_data = self.analyze_products(top_n)
        sns.set_style('whitegrid')
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Top by sales
        sns.barplot(x='total_sales', y='coffee_name', 
                   data=product_data['top_by_sales'], 
                   ax=axes[0], color='coral')
        axes[0].set_title(f'Top {top_n} Products by Sales', fontsize=14)
        axes[0].set_xlabel('Total Sales ($)', fontsize=12)
        axes[0].set_ylabel('Product', fontsize=12)
        
        # Top by items sold
        sns.barplot(x='items_sold', y='coffee_name', 
                   data=product_data['top_by_items_sold'], 
                   ax=axes[1], color='teal')
        axes[1].set_title(f'Top {top_n} Products by Items Sold', fontsize=14)
        axes[1].set_xlabel('Items Sold', fontsize=12)
        axes[1].set_ylabel('Product', fontsize=12)
        
        plt.tight_layout()
        
        if save:
            plt.savefig('top_products_analysis.png', dpi=150)
            print("Saved: top_products_analysis.png")
        if show:
            plt.show()
        plt.close()
    
    def plot_hourly_analysis(self, save=True, show=False):
        """Visualize hourly sales patterns for operations planning."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        hourly_data = self.analyze_hourly_sales()['hourly_stats']
        sns.set_style('whitegrid')
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Hourly sales
        axes[0].bar(hourly_data['hour'], hourly_data['total_sales'], color='steelblue', alpha=0.7)
        axes[0].set_title('Sales by Hour of Day', fontsize=14)
        axes[0].set_xlabel('Hour', fontsize=12)
        axes[0].set_ylabel('Total Sales ($)', fontsize=12)
        axes[0].set_xticks(range(0, 24))
        
        # Highlight peak hours
        peak_hours = self.analyze_hourly_sales()['peak_hours']
        for hour in peak_hours:
            axes[0].axvline(x=hour, color='red', linestyle='--', alpha=0.5, label='Peak Hour' if hour == peak_hours[0] else '')
        axes[0].legend()
        
        # Transaction count by hour
        axes[1].bar(hourly_data['hour'], hourly_data['transaction_count'], color='forestgreen', alpha=0.7)
        axes[1].set_title('Number of Transactions by Hour', fontsize=14)
        axes[1].set_xlabel('Hour', fontsize=12)
        axes[1].set_ylabel('Transactions', fontsize=12)
        axes[1].set_xticks(range(0, 24))
        
        plt.tight_layout()
        
        if save:
            plt.savefig('hourly_sales_analysis.png', dpi=150)
            print("Saved: hourly_sales_analysis.png")
        if show:
            plt.show()
        plt.close()
    
    def plot_daily_trends(self, save=True, show=False):
        """Visualize daily sales trends with moving average."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        daily_data = self.get_daily_sales_trend()
        sns.set_style('whitegrid')
        
        plt.figure(figsize=(14, 7))
        plt.plot(daily_data.index, daily_data['total_sales'], 
                marker='o', linestyle='-', alpha=0.5, label='Daily Sales', color='blue')
        plt.plot(daily_data.index, daily_data['moving_avg_7d'], 
                linewidth=2, label='7-Day Moving Average', color='red')
        
        plt.title('Daily Sales Trend with Moving Average', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save:
            plt.savefig('daily_sales_trend.png', dpi=150)
            print("Saved: daily_sales_trend.png")
        if show:
            plt.show()
        plt.close()
    
    def plot_weekly_comparison(self, save=True, show=False):
        """Visualize sales by day of week."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        daily_stats = self.analyze_daily_sales()['daily_stats']
        sns.set_style('whitegrid')
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(daily_stats['day_name'], daily_stats['total_sales'], color='purple', alpha=0.7)
        
        # Highlight busiest day - find position in the sorted dataframe
        busiest_idx = daily_stats['total_sales'].idxmax()
        bar_position = daily_stats.index.get_loc(busiest_idx)
        bars[bar_position].set_color('gold')
        
        plt.title('Sales by Day of Week', fontsize=14)
        plt.xlabel('Day', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save:
            plt.savefig('weekly_sales_comparison.png', dpi=150)
            print("Saved: weekly_sales_comparison.png")
        if show:
            plt.show()
        plt.close()
    
    def plot_inventory_velocity(self, save=True, show=False):
        """Visualize product velocity for inventory management."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        inv_rec = self.get_inventory_recommendations()
        velocity_data = inv_rec['product_velocity'].sort_values('daily_velocity', ascending=True).tail(15)
        
        sns.set_style('whitegrid')
        plt.figure(figsize=(12, 8))
        
        colors = {'High': 'green', 'Medium': 'orange', 'Low': 'red'}
        bar_colors = [colors[v] for v in velocity_data['velocity_class']]
        
        plt.barh(velocity_data['product'], velocity_data['daily_velocity'], color=bar_colors)
        plt.xlabel('Daily Sales Velocity (units/day)', fontsize=12)
        plt.ylabel('Product', fontsize=12)
        plt.title('Product Sales Velocity (Top 15)', fontsize=14)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='green', label='High Velocity'),
                          Patch(facecolor='orange', label='Medium Velocity'),
                          Patch(facecolor='red', label='Low Velocity')]
        plt.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        
        if save:
            plt.savefig('product_velocity.png', dpi=150)
            print("Saved: product_velocity.png")
        if show:
            plt.show()
        plt.close()
    
    # --- REPORTS ---
    
    def generate_operations_report(self):
        """
        Generate a comprehensive operations report with key insights
        for optimizing coffee shop operations.
        """
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        print("\n" + "="*60)
        print("COFFEE OPERATIONS ANALYTICS REPORT")
        print("="*60)
        
        # Descriptive stats
        stats = self.get_descriptive_stats()
        print("\n--- SALES OVERVIEW ---")
        print(f"Total Revenue: ${stats['total_sales']:,.2f}")
        print(f"Total Transactions: {stats['total_transactions']:,}")
        print(f"Average Transaction: ${stats['average_transaction']:.2f}")
        print(f"Unique Products: {stats['unique_products']}")
        
        # Hourly analysis
        hourly = self.analyze_hourly_sales()
        print("\n--- PEAK HOURS ANALYSIS ---")
        print(f"Peak Hours: {hourly['peak_hours']}")
        print(f"Slow Hours: {hourly['slow_hours']}")
        print(f"Recommendation: {hourly['recommendation']}")
        
        # Daily analysis
        daily = self.analyze_daily_sales()
        print("\n--- DAILY PATTERNS ---")
        print(f"Busiest Day: {daily['busiest_day']}")
        print(f"Slowest Day: {daily['slowest_day']}")
        
        # Top products
        products = self.analyze_products(5)
        print("\n--- TOP 5 PRODUCTS BY SALES ---")
        for _, row in products['top_by_sales'].iterrows():
            print(f"  {row['coffee_name']}: ${row['total_sales']:.2f} ({row['sales_percentage']}%)")
        
        # Inventory recommendations
        inv = self.get_inventory_recommendations()
        print("\n--- INVENTORY RECOMMENDATIONS ---")
        for insight in inv['insights']:
            print(f"  • {insight}")
        
        print("\n" + "="*60)
        return {
            'stats': stats,
            'hourly': hourly,
            'daily': daily,
            'products': products,
            'inventory': inv
        }
    
    def export_analysis_to_csv(self, prefix='analysis'):
        """Export analysis results to CSV files."""
        if not self.cleaned:
            raise ValueError("Data not cleaned. Call clean_data() first.")
        
        # Export cleaned data
        self.df.to_csv(f'{prefix}_cleaned_data.csv', index=False)
        
        # Export product analysis
        products = self.analyze_products()
        products['full_analysis'].to_csv(f'{prefix}_products.csv', index=False)
        
        # Export hourly stats
        hourly = self.analyze_hourly_sales()
        hourly['hourly_stats'].to_csv(f'{prefix}_hourly_stats.csv', index=False)
        
        # Export daily stats
        daily = self.analyze_daily_sales()
        daily['daily_stats'].to_csv(f'{prefix}_daily_stats.csv', index=False)
        
        # Export inventory recommendations
        inv = self.get_inventory_recommendations()
        inv['product_velocity'].to_csv(f'{prefix}_product_velocity.csv', index=False)
        
        print(f"Exported analysis files with prefix: {prefix}_")
    
    def run_full_analysis(self, generate_plots=True, export_csv=True):
        """
        Run complete analysis pipeline.
        Convenience method for full analytics workflow.
        """
        print("Starting full analytics pipeline...")
        
        # Generate report
        report = self.generate_operations_report()
        
        # Generate visualizations
        if generate_plots:
            print("\nGenerating visualizations...")
            self.plot_top_products()
            self.plot_hourly_analysis()
            self.plot_daily_trends()
            self.plot_weekly_comparison()
            self.plot_inventory_velocity()
        
        # Export to CSV
        if export_csv:
            print("\nExporting analysis to CSV...")
            self.export_analysis_to_csv()
        
        print("\n✓ Full analysis complete!")
        return report


# --- Main execution ---
if __name__ == "__main__":
    # Initialize analytics
    analytics = CoffeeAnalytics('coffee sales dataset.csv')
    
    try:
        # Load and clean data
        analytics.load_data()
        analytics.clean_data()
        
        # Run full analysis
        analytics.run_full_analysis(generate_plots=True, export_csv=True)
        
    except FileNotFoundError:
        print("Error: 'coffee sales dataset.csv' not found.")
        print("Please ensure the data file is in the current directory.")
    except Exception as e:
        print(f"Error during analysis: {e}")
