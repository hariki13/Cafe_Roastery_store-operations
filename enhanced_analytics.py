# --- Enhanced Data Analytics for Specialty Coffee Shop with Bakery & Cake ---
# This module provides comprehensive data analysis capabilities for coffee shop operations
# including bakery and cake product categories

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy import stats


class CoffeeShopAnalytics:
    """
    A comprehensive analytics class for specialty coffee shop operations
    including coffee, bakery, and cake product categories.
    """

    def __init__(self, data_path=None, dataframe=None):
        """
        Initialize the analytics class with data from file or DataFrame.

        Args:
            data_path: Path to CSV file containing sales data
            dataframe: Pandas DataFrame with sales data
        """
        if dataframe is not None:
            self.df = dataframe.copy()
        elif data_path is not None:
            self.df = pd.read_csv(data_path)
        else:
            self.df = None

        self.cleaned = False
        self.product_categories = {
            'coffee': ['americano', 'latte', 'cappuccino', 'espresso', 'mocha',
                      'macchiato', 'flat white', 'cold brew', 'coffee'],
            'bakery': ['croissant', 'muffin', 'bagel', 'bread', 'danish',
                      'scone', 'cookie', 'brownie', 'pastry'],
            'cake': ['cake', 'cheesecake', 'tiramisu', 'cupcake', 'tart',
                    'pie', 'slice']
        }

    def load_data(self, file_path):
        """Load data from CSV file."""
        self.df = pd.read_csv(file_path)
        self.cleaned = False
        return self

    def get_data_overview(self):
        """Get comprehensive overview of the dataset."""
        if self.df is None:
            raise ValueError("No data loaded. Please load data first.")

        overview = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        }
        return overview

    def clean_data(self, datetime_col='datetime', amount_col='money',
                   product_col='coffee_name'):
        """
        Clean and preprocess the data for analysis.

        Args:
            datetime_col: Name of the datetime column
            amount_col: Name of the sales amount column
            product_col: Name of the product name column
        """
        if self.df is None:
            raise ValueError("No data loaded. Please load data first.")

        initial_rows = len(self.df)
        cleaning_report = {'initial_rows': initial_rows}

        # Convert datetime column
        if datetime_col in self.df.columns:
            self.df[datetime_col] = pd.to_datetime(self.df[datetime_col], errors='coerce')

        # Track missing values before cleaning
        cleaning_report['missing_before'] = self.df.isnull().sum().to_dict()

        # Remove rows with missing critical values
        critical_columns = [col for col in [datetime_col, amount_col, product_col]
                          if col in self.df.columns]
        self.df.dropna(subset=critical_columns, inplace=True)

        # Remove duplicates
        duplicates_removed = len(self.df)
        self.df.drop_duplicates(inplace=True)
        cleaning_report['duplicates_removed'] = duplicates_removed - len(self.df)

        # Clean amount column - ensure numeric
        if amount_col in self.df.columns:
            self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
            self.df = self.df[self.df[amount_col] > 0]  # Remove zero or negative sales

        # Add derived columns for analysis
        if datetime_col in self.df.columns:
            self.df['date'] = self.df[datetime_col].dt.date
            self.df['hour'] = self.df[datetime_col].dt.hour
            self.df['day_of_week'] = self.df[datetime_col].dt.day_name()
            self.df['week'] = self.df[datetime_col].dt.isocalendar().week
            self.df['month'] = self.df[datetime_col].dt.month
            self.df['month_name'] = self.df[datetime_col].dt.month_name()
            self.df['year'] = self.df[datetime_col].dt.year
            self.df['is_weekend'] = self.df[datetime_col].dt.dayofweek >= 5

        # Categorize products
        if product_col in self.df.columns:
            self.df['product_category'] = self.df[product_col].apply(
                self._categorize_product
            )

        cleaning_report['final_rows'] = len(self.df)
        cleaning_report['rows_removed'] = initial_rows - len(self.df)

        self.cleaned = True
        return cleaning_report

    def _categorize_product(self, product_name):
        """Categorize a product based on its name."""
        if pd.isna(product_name):
            return 'other'

        product_lower = str(product_name).lower()
        for category, keywords in self.product_categories.items():
            if any(keyword in product_lower for keyword in keywords):
                return category
        return 'other'

    def add_custom_category(self, category_name, keywords):
        """Add a custom product category with keywords."""
        self.product_categories[category_name] = keywords
        if self.cleaned and 'coffee_name' in self.df.columns:
            self.df['product_category'] = self.df['coffee_name'].apply(
                self._categorize_product
            )

    def get_descriptive_statistics(self, amount_col='money'):
        """
        Get comprehensive descriptive statistics for sales data.

        Args:
            amount_col: Name of the sales amount column

        Returns:
            Dictionary containing descriptive statistics
        """
        if self.df is None or amount_col not in self.df.columns:
            raise ValueError(f"Column '{amount_col}' not found in data.")

        sales_data = self.df[amount_col]

        if len(sales_data) == 0:
            return {
                'count': 0, 'total': 0, 'mean': None, 'median': None,
                'mode': None, 'std_dev': None, 'variance': None,
                'min': None, 'max': None, 'range': None,
                'q1': None, 'q3': None, 'iqr': None,
                'skewness': None, 'kurtosis': None
            }

        mode_series = sales_data.mode()
        mode_value = mode_series.iloc[0] if len(mode_series) > 0 else None

        stats_dict = {
            'count': len(sales_data),
            'total': sales_data.sum(),
            'mean': sales_data.mean(),
            'median': sales_data.median(),
            'mode': mode_value,
            'std_dev': sales_data.std(),
            'variance': sales_data.var(),
            'min': sales_data.min(),
            'max': sales_data.max(),
            'range': sales_data.max() - sales_data.min(),
            'q1': sales_data.quantile(0.25),
            'q3': sales_data.quantile(0.75),
            'iqr': sales_data.quantile(0.75) - sales_data.quantile(0.25),
            'skewness': stats.skew(sales_data),
            'kurtosis': stats.kurtosis(sales_data)
        }
        return stats_dict

    def get_product_analysis(self, product_col='coffee_name', amount_col='money'):
        """
        Analyze sales by product with comprehensive metrics.

        Args:
            product_col: Name of the product column
            amount_col: Name of the sales amount column

        Returns:
            DataFrame with product analysis
        """
        if self.df is None:
            raise ValueError("No data loaded. Please load data first.")

        analysis = self.df.groupby(product_col)[amount_col].agg([
            ('total_sales', 'sum'),
            ('items_sold', 'count'),
            ('avg_price', 'mean'),
            ('median_price', 'median'),
            ('min_price', 'min'),
            ('max_price', 'max'),
            ('std_dev', 'std')
        ]).reset_index()

        # Add percentage of total sales
        analysis['sales_percentage'] = (
            analysis['total_sales'] / analysis['total_sales'].sum() * 100
        )

        return analysis.sort_values('total_sales', ascending=False)

    def get_category_analysis(self, amount_col='money'):
        """
        Analyze sales by product category (coffee, bakery, cake, other).

        Args:
            amount_col: Name of the sales amount column

        Returns:
            DataFrame with category analysis
        """
        if 'product_category' not in self.df.columns:
            raise ValueError("Product categories not available. Run clean_data() first.")

        analysis = self.df.groupby('product_category')[amount_col].agg([
            ('total_sales', 'sum'),
            ('items_sold', 'count'),
            ('avg_sale', 'mean'),
            ('median_sale', 'median')
        ]).reset_index()

        analysis['sales_percentage'] = (
            analysis['total_sales'] / analysis['total_sales'].sum() * 100
        )

        return analysis.sort_values('total_sales', ascending=False)

    def get_time_analysis(self, amount_col='money', period='day'):
        """
        Analyze sales by time period.

        Args:
            amount_col: Name of the sales amount column
            period: Time period ('hour', 'day', 'week', 'month')

        Returns:
            DataFrame or Series with time-based analysis
        """
        if self.df is None:
            raise ValueError("No data loaded. Please load data first.")

        if period == 'hour':
            return self.df.groupby('hour')[amount_col].agg(['sum', 'count', 'mean'])
        elif period == 'day':
            return self.df.groupby('date')[amount_col].agg(['sum', 'count', 'mean'])
        elif period == 'day_of_week':
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']
            analysis = self.df.groupby('day_of_week')[amount_col].agg(['sum', 'count', 'mean'])
            return analysis.reindex(day_order)
        elif period == 'week':
            return self.df.groupby('week')[amount_col].agg(['sum', 'count', 'mean'])
        elif period == 'month':
            return self.df.groupby(['year', 'month'])[amount_col].agg(['sum', 'count', 'mean'])
        else:
            raise ValueError(f"Invalid period: {period}")

    def get_peak_hours_analysis(self, amount_col='money'):
        """
        Identify peak hours for sales.

        Returns:
            Dictionary with peak hours analysis
        """
        hourly = self.df.groupby('hour').agg({
            amount_col: ['sum', 'count', 'mean']
        }).reset_index()
        hourly.columns = ['hour', 'total_sales', 'transactions', 'avg_sale']

        peak_sales_hour = hourly.loc[hourly['total_sales'].idxmax()]
        peak_transactions_hour = hourly.loc[hourly['transactions'].idxmax()]

        return {
            'hourly_breakdown': hourly,
            'peak_sales_hour': int(peak_sales_hour['hour']),
            'peak_sales_amount': peak_sales_hour['total_sales'],
            'peak_transactions_hour': int(peak_transactions_hour['hour']),
            'peak_transactions_count': peak_transactions_hour['transactions']
        }

    def get_weekend_vs_weekday_analysis(self, amount_col='money'):
        """
        Compare weekend vs weekday sales.

        Returns:
            Dictionary with comparison analysis
        """
        weekend = self.df[self.df['is_weekend']]
        weekday = self.df[~self.df['is_weekend']]

        return {
            'weekend': {
                'total_sales': weekend[amount_col].sum(),
                'avg_sale': weekend[amount_col].mean(),
                'transactions': len(weekend),
                'avg_transaction_per_day': len(weekend) / max(weekend['date'].nunique(), 1)
            },
            'weekday': {
                'total_sales': weekday[amount_col].sum(),
                'avg_sale': weekday[amount_col].mean(),
                'transactions': len(weekday),
                'avg_transaction_per_day': len(weekday) / max(weekday['date'].nunique(), 1)
            }
        }

    def get_top_products(self, n=10, by='sales', product_col='coffee_name',
                         amount_col='money'):
        """
        Get top N products by sales or quantity.

        Args:
            n: Number of top products to return
            by: 'sales' or 'quantity'
            product_col: Name of the product column
            amount_col: Name of the sales amount column

        Returns:
            DataFrame with top products
        """
        analysis = self.get_product_analysis(product_col, amount_col)

        if by == 'sales':
            return analysis.head(n)
        elif by == 'quantity':
            return analysis.sort_values('items_sold', ascending=False).head(n)
        else:
            raise ValueError(f"Invalid 'by' parameter: {by}")

    def detect_outliers(self, amount_col='money', method='iqr'):
        """
        Detect outliers in sales data.

        Args:
            amount_col: Name of the sales amount column
            method: 'iqr' or 'zscore'

        Returns:
            Dictionary with outlier information
        """
        data = self.df[amount_col]

        if method == 'iqr':
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = self.df[(data < lower_bound) | (data > upper_bound)]
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outliers = self.df[z_scores > 3]
            lower_bound = data.mean() - 3 * data.std()
            upper_bound = data.mean() + 3 * data.std()
        else:
            raise ValueError(f"Invalid method: {method}")

        return {
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(self.df) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers': outliers
        }

    def calculate_growth_rate(self, amount_col='money', period='month'):
        """
        Calculate sales growth rate over time.

        Args:
            amount_col: Name of the sales amount column
            period: 'day', 'week', or 'month'

        Returns:
            DataFrame with growth rates
        """
        if period == 'day':
            grouped = self.df.groupby('date')[amount_col].sum().reset_index()
            grouped.columns = ['period', 'sales']
        elif period == 'week':
            grouped = self.df.groupby('week')[amount_col].sum().reset_index()
            grouped.columns = ['period', 'sales']
        elif period == 'month':
            grouped = self.df.groupby(['year', 'month'])[amount_col].sum().reset_index()
            grouped['period'] = grouped['year'].astype(str) + '-' + grouped['month'].astype(str).str.zfill(2)
            grouped = grouped[['period', amount_col]].rename(columns={amount_col: 'sales'})
        else:
            raise ValueError(f"Invalid period: {period}")

        grouped['growth_rate'] = grouped['sales'].pct_change() * 100
        grouped['cumulative_sales'] = grouped['sales'].cumsum()

        return grouped

    # --- Visualization Methods ---

    def plot_sales_distribution(self, amount_col='money', save_path=None):
        """Plot distribution of sales amounts."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        axes[0].hist(self.df[amount_col], bins=30, edgecolor='black', alpha=0.7)
        axes[0].set_title('Sales Distribution (Histogram)', fontsize=14)
        axes[0].set_xlabel('Sale Amount ($)', fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)

        # Box plot
        axes[1].boxplot(self.df[amount_col], vert=True)
        axes[1].set_title('Sales Distribution (Box Plot)', fontsize=14)
        axes[1].set_ylabel('Sale Amount ($)', fontsize=12)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def plot_top_products(self, n=10, by='sales', product_col='coffee_name',
                          amount_col='money', save_path=None):
        """Plot top N products."""
        top = self.get_top_products(n, by, product_col, amount_col)

        fig, ax = plt.subplots(figsize=(12, 6))

        if by == 'sales':
            sns.barplot(x='total_sales', y=product_col, data=top,
                       hue=product_col, palette='viridis', ax=ax, legend=False)
            ax.set_xlabel('Total Sales ($)', fontsize=12)
            ax.set_title(f'Top {n} Products by Sales', fontsize=14)
        else:
            sns.barplot(x='items_sold', y=product_col, data=top,
                       hue=product_col, palette='viridis', ax=ax, legend=False)
            ax.set_xlabel('Items Sold', fontsize=12)
            ax.set_title(f'Top {n} Products by Quantity', fontsize=14)

        ax.set_ylabel('Product', fontsize=12)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def plot_category_breakdown(self, amount_col='money', save_path=None):
        """Plot sales breakdown by product category."""
        category_data = self.get_category_analysis(amount_col)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Pie chart
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f39c12']
        axes[0].pie(category_data['total_sales'],
                   labels=category_data['product_category'],
                   autopct='%1.1f%%', colors=colors[:len(category_data)],
                   explode=[0.05] * len(category_data))
        axes[0].set_title('Sales by Category (Pie Chart)', fontsize=14)

        # Bar chart
        sns.barplot(x='product_category', y='total_sales',
                   data=category_data, hue='product_category',
                   palette='viridis', ax=axes[1], legend=False)
        axes[1].set_title('Sales by Category (Bar Chart)', fontsize=14)
        axes[1].set_xlabel('Category', fontsize=12)
        axes[1].set_ylabel('Total Sales ($)', fontsize=12)
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def plot_daily_trend(self, amount_col='money', datetime_col='datetime', save_path=None):
        """Plot daily sales trend."""
        if datetime_col not in self.df.columns:
            raise ValueError(f"Column '{datetime_col}' not found. Run clean_data() first.")

        daily = self.df.set_index(datetime_col).resample('D')[amount_col].sum()

        fig, ax = plt.subplots(figsize=(14, 6))
        daily.plot(kind='line', marker='o', color='blue',
                  linestyle='-', linewidth=1, markersize=4, ax=ax)

        # Add trend line
        x = np.arange(len(daily))
        z = np.polyfit(x, daily.values, 1)
        p = np.poly1d(z)
        ax.plot(daily.index, p(x), "r--", alpha=0.8, label='Trend')

        ax.set_title('Daily Sales Trend', fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Sales ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def plot_hourly_heatmap(self, amount_col='money', save_path=None):
        """Plot heatmap of sales by hour and day of week."""
        pivot = self.df.pivot_table(
            values=amount_col,
            index='hour',
            columns='day_of_week',
            aggfunc='sum'
        )

        # Reorder columns
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']
        pivot = pivot.reindex(columns=[d for d in day_order if d in pivot.columns])

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
        ax.set_title('Sales Heatmap by Hour and Day', fontsize=14)
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Hour', fontsize=12)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def plot_monthly_comparison(self, amount_col='money', save_path=None):
        """Plot monthly sales comparison."""
        monthly = self.df.groupby(['year', 'month_name'])[amount_col].sum().reset_index()

        fig, ax = plt.subplots(figsize=(14, 6))
        sns.barplot(x='month_name', y=amount_col, hue='year', data=monthly, ax=ax)
        ax.set_title('Monthly Sales Comparison', fontsize=14)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Year')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def generate_comprehensive_report(self, output_dir='.'):
        """
        Generate a comprehensive analytics report with all visualizations.

        Args:
            output_dir: Directory to save report files

        Returns:
            Dictionary with all analysis results
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        report = {
            'generated_at': datetime.now().isoformat(),
            'descriptive_statistics': self.get_descriptive_statistics(),
            'product_analysis': self.get_product_analysis().to_dict('records'),
            'category_analysis': self.get_category_analysis().to_dict('records'),
            'peak_hours': self.get_peak_hours_analysis(),
            'weekend_vs_weekday': self.get_weekend_vs_weekday_analysis(),
            'outliers': {
                k: v for k, v in self.detect_outliers().items()
                if k != 'outliers'
            }
        }

        # Generate and save visualizations
        self.plot_top_products(save_path=f'{output_dir}/top_products.png')
        self.plot_category_breakdown(save_path=f'{output_dir}/category_breakdown.png')
        self.plot_daily_trend(save_path=f'{output_dir}/daily_trend.png')
        self.plot_hourly_heatmap(save_path=f'{output_dir}/hourly_heatmap.png')
        self.plot_sales_distribution(save_path=f'{output_dir}/sales_distribution.png')

        plt.close('all')

        return report

    def export_analysis(self, filename, format='csv'):
        """
        Export analyzed data to file.

        Args:
            filename: Output filename
            format: 'csv', 'excel', or 'json'
        """
        if format == 'csv':
            self.df.to_csv(filename, index=False)
        elif format == 'excel':
            self.df.to_excel(filename, index=False)
        elif format == 'json':
            self.df.to_json(filename, orient='records', date_format='iso')
        else:
            raise ValueError(f"Unsupported format: {format}")


# Default data file path constant
DEFAULT_DATA_FILE = 'coffee sales dataset.csv'


def run_demo_analysis(data_file=None):
    """
    Run a demonstration analysis with sample data or existing file.

    Args:
        data_file: Path to the data file. If None, uses DEFAULT_DATA_FILE.
    """
    import os

    if data_file is None:
        data_file = DEFAULT_DATA_FILE

    if not os.path.exists(data_file):
        print("No data file found. Creating sample data for demonstration...")
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=1000, freq='h')
        products = ['Latte', 'Cappuccino', 'Americano', 'Espresso', 'Mocha',
                   'Croissant', 'Muffin', 'Chocolate Cake', 'Cheesecake', 'Scone']

        sample_df = pd.DataFrame({
            'datetime': np.random.choice(dates, 1000),
            'coffee_name': np.random.choice(products, 1000),
            'money': np.random.uniform(2.5, 15.0, 1000).round(2)
        })
        sample_df.to_csv(data_file, index=False)
        print(f"Sample data saved to {data_file}")

    # Initialize analytics
    analytics = CoffeeShopAnalytics(data_path=data_file)

    # Run analysis
    print("\n" + "="*60)
    print("SPECIALTY COFFEE SHOP - ENHANCED DATA ANALYTICS")
    print("="*60)

    # Data Overview
    overview = analytics.get_data_overview()
    print(f"\n📊 DATA OVERVIEW:")
    print(f"   Total Records: {overview['total_rows']}")
    print(f"   Total Columns: {overview['total_columns']}")

    # Clean Data
    cleaning_report = analytics.clean_data()
    print(f"\n🧹 DATA CLEANING:")
    print(f"   Initial Rows: {cleaning_report['initial_rows']}")
    print(f"   Final Rows: {cleaning_report['final_rows']}")
    print(f"   Duplicates Removed: {cleaning_report['duplicates_removed']}")

    # Descriptive Statistics
    stats = analytics.get_descriptive_statistics()
    print(f"\n📈 DESCRIPTIVE STATISTICS:")
    print(f"   Total Sales: ${stats['total']:,.2f}")
    print(f"   Average Sale: ${stats['mean']:,.2f}")
    print(f"   Median Sale: ${stats['median']:,.2f}")
    print(f"   Std Deviation: ${stats['std_dev']:,.2f}")
    print(f"   Min Sale: ${stats['min']:,.2f}")
    print(f"   Max Sale: ${stats['max']:,.2f}")

    # Category Analysis
    category_analysis = analytics.get_category_analysis()
    print(f"\n🏷️  CATEGORY ANALYSIS:")
    for _, row in category_analysis.iterrows():
        print(f"   {row['product_category'].upper()}:")
        print(f"      Sales: ${row['total_sales']:,.2f} ({row['sales_percentage']:.1f}%)")
        print(f"      Items: {row['items_sold']}")

    # Peak Hours
    peak = analytics.get_peak_hours_analysis()
    print(f"\n⏰ PEAK HOURS:")
    print(f"   Peak Sales Hour: {peak['peak_sales_hour']}:00")
    print(f"   Peak Transactions Hour: {peak['peak_transactions_hour']}:00")

    # Weekend vs Weekday
    weekend_analysis = analytics.get_weekend_vs_weekday_analysis()
    print(f"\n📅 WEEKEND VS WEEKDAY:")
    print(f"   Weekend Sales: ${weekend_analysis['weekend']['total_sales']:,.2f}")
    print(f"   Weekday Sales: ${weekend_analysis['weekday']['total_sales']:,.2f}")

    # Top Products
    top_5 = analytics.get_top_products(5)
    print("\n🏆 TOP 5 PRODUCTS:")
    for rank, (_, row) in enumerate(top_5.iterrows(), start=1):
        print(f"   {rank}. {row['coffee_name']}: ${row['total_sales']:,.2f}")

    # Generate Report
    print("\n📊 Generating comprehensive report...")
    analytics.generate_comprehensive_report(output_dir='analytics_output')
    print("   Report generated in 'analytics_output' directory")

    # Export cleaned data
    analytics.export_analysis('cleaned_sales_data.csv')
    print("\n💾 Cleaned data exported to 'cleaned_sales_data.csv'")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    return analytics


if __name__ == "__main__":
    run_demo_analysis()
