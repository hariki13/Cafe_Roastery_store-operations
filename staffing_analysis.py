# --- Staffing Operations Analysis Based on Peak and Low Hours ---
# This module analyzes sales data to identify peak and low traffic hours
# and provides staffing recommendations for optimal store operations.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Step 1: Load and Prepare Data ---
def load_and_prepare_data(filepath='coffee sales dataset.csv'):
    """Load data and prepare it for hourly analysis."""
    df = pd.read_csv(filepath)
    
    # Convert datetime column
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    
    # Remove rows with missing critical data
    df.dropna(subset=['datetime', 'money', 'coffee_name'], inplace=True)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Extract hour from datetime for hourly analysis
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['date'] = df['datetime'].dt.date
    
    return df


# --- Step 2: Hourly Traffic Analysis ---
def analyze_hourly_patterns(df):
    """Analyze sales patterns by hour of day."""
    # Group by hour and calculate metrics
    hourly_analysis = df.groupby('hour').agg(
        total_sales=('money', 'sum'),
        transaction_count=('money', 'count'),
        average_transaction=('money', 'mean')
    ).reset_index()
    
    return hourly_analysis


# --- Step 3: Identify Peak and Low Hours ---
def identify_peak_low_hours(hourly_analysis):
    """Identify peak and low traffic hours based on transaction count."""
    # Calculate percentiles for classification
    high_threshold = hourly_analysis['transaction_count'].quantile(0.75)
    low_threshold = hourly_analysis['transaction_count'].quantile(0.25)
    
    # Classify hours
    def classify_hour(count):
        if count >= high_threshold:
            return 'Peak'
        elif count <= low_threshold:
            return 'Low'
        else:
            return 'Normal'
    
    hourly_analysis['traffic_level'] = hourly_analysis['transaction_count'].apply(classify_hour)
    
    peak_hours = hourly_analysis[hourly_analysis['traffic_level'] == 'Peak']['hour'].tolist()
    low_hours = hourly_analysis[hourly_analysis['traffic_level'] == 'Low']['hour'].tolist()
    normal_hours = hourly_analysis[hourly_analysis['traffic_level'] == 'Normal']['hour'].tolist()
    
    return hourly_analysis, peak_hours, low_hours, normal_hours


# --- Step 4: Day of Week Analysis ---
def analyze_day_of_week_patterns(df):
    """Analyze sales patterns by day of the week."""
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    daily_analysis = df.groupby('day_of_week').agg(
        total_sales=('money', 'sum'),
        transaction_count=('money', 'count'),
        average_transaction=('money', 'mean')
    ).reindex(day_order).reset_index()
    
    return daily_analysis


# --- Step 5: Staffing Recommendations ---
def generate_staffing_recommendations(hourly_analysis, base_staff=2):
    """
    Generate staffing recommendations based on hourly traffic patterns.
    
    Parameters:
    - hourly_analysis: DataFrame with hourly traffic data
    - base_staff: Minimum number of staff during low hours
    
    Returns:
    - DataFrame with staffing recommendations
    """
    # Calculate staff multiplier based on traffic level
    max_transactions = hourly_analysis['transaction_count'].max()
    min_transactions = hourly_analysis['transaction_count'].min()
    
    def calculate_staff(row):
        if max_transactions == min_transactions or max_transactions == 0:
            return base_staff
        
        # Normalize transaction count to staff level
        normalized = (row['transaction_count'] - min_transactions) / (max_transactions - min_transactions)
        
        # Scale staff: low hours = base_staff, peak hours = base_staff * 3
        recommended = base_staff + (normalized * (base_staff * 2))
        return int(np.ceil(recommended))
    
    hourly_analysis['recommended_staff'] = hourly_analysis.apply(calculate_staff, axis=1)
    
    return hourly_analysis


# --- Step 6: Visualizations ---
def create_visualizations(hourly_analysis, daily_analysis, output_prefix='staffing'):
    """Create visualizations for staffing analysis."""
    sns.set_style('whitegrid')
    
    # 1. Hourly Transaction Pattern
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Hourly transactions bar chart
    colors = ['red' if level == 'Peak' else 'green' if level == 'Low' else 'blue' 
              for level in hourly_analysis['traffic_level']]
    
    axes[0, 0].bar(hourly_analysis['hour'], hourly_analysis['transaction_count'], color=colors)
    axes[0, 0].set_title('Transactions by Hour (Red=Peak, Green=Low, Blue=Normal)', fontsize=14)
    axes[0, 0].set_xlabel('Hour of Day', fontsize=12)
    axes[0, 0].set_ylabel('Number of Transactions', fontsize=12)
    axes[0, 0].set_xticks(range(0, 24))
    
    # Hourly sales
    axes[0, 1].plot(hourly_analysis['hour'], hourly_analysis['total_sales'], 
                   marker='o', color='purple', linewidth=2)
    axes[0, 1].fill_between(hourly_analysis['hour'], hourly_analysis['total_sales'], alpha=0.3)
    axes[0, 1].set_title('Total Sales by Hour', fontsize=14)
    axes[0, 1].set_xlabel('Hour of Day', fontsize=12)
    axes[0, 1].set_ylabel('Total Sales ($)', fontsize=12)
    axes[0, 1].set_xticks(range(0, 24))
    
    # Recommended staff
    axes[1, 0].bar(hourly_analysis['hour'], hourly_analysis['recommended_staff'], color='teal')
    axes[1, 0].set_title('Recommended Staff by Hour', fontsize=14)
    axes[1, 0].set_xlabel('Hour of Day', fontsize=12)
    axes[1, 0].set_ylabel('Number of Staff', fontsize=12)
    axes[1, 0].set_xticks(range(0, 24))
    
    # Day of week transactions
    if daily_analysis is not None and len(daily_analysis) > 0:
        axes[1, 1].bar(range(len(daily_analysis)), daily_analysis['transaction_count'], color='orange')
        axes[1, 1].set_title('Transactions by Day of Week', fontsize=14)
        axes[1, 1].set_xlabel('Day of Week', fontsize=12)
        axes[1, 1].set_ylabel('Number of Transactions', fontsize=12)
        axes[1, 1].set_xticks(range(len(daily_analysis)))
        axes[1, 1].set_xticklabels(daily_analysis['day_of_week'], rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_analysis.png', dpi=150)
    print(f"\nSaved '{output_prefix}_analysis.png'")
    plt.close(fig)
    
    return fig


# --- Step 7: Generate Summary Report ---
def generate_summary_report(hourly_analysis, peak_hours, low_hours, daily_analysis):
    """Generate a text summary of staffing recommendations."""
    report = []
    report.append("=" * 60)
    report.append("STAFFING OPERATIONS ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Peak hours summary
    report.append("PEAK HOURS (High Traffic):")
    report.append("-" * 30)
    for hour in sorted(peak_hours):
        hour_data = hourly_analysis[hourly_analysis['hour'] == hour].iloc[0]
        report.append(f"  {hour:02d}:00 - Transactions: {hour_data['transaction_count']:.0f}, "
                     f"Sales: ${hour_data['total_sales']:.2f}, "
                     f"Recommended Staff: {hour_data['recommended_staff']}")
    report.append("")
    
    # Low hours summary
    report.append("LOW HOURS (Low Traffic):")
    report.append("-" * 30)
    for hour in sorted(low_hours):
        hour_data = hourly_analysis[hourly_analysis['hour'] == hour].iloc[0]
        report.append(f"  {hour:02d}:00 - Transactions: {hour_data['transaction_count']:.0f}, "
                     f"Sales: ${hour_data['total_sales']:.2f}, "
                     f"Recommended Staff: {hour_data['recommended_staff']}")
    report.append("")
    
    # Staffing summary
    report.append("STAFFING RECOMMENDATIONS:")
    report.append("-" * 30)
    total_staff_hours = hourly_analysis['recommended_staff'].sum()
    avg_staff = hourly_analysis['recommended_staff'].mean()
    max_staff = hourly_analysis['recommended_staff'].max()
    min_staff = hourly_analysis['recommended_staff'].min()
    
    report.append(f"  Total Daily Staff Hours: {total_staff_hours}")
    report.append(f"  Average Staff per Hour: {avg_staff:.1f}")
    report.append(f"  Peak Hour Staff: {max_staff}")
    report.append(f"  Low Hour Staff: {min_staff}")
    report.append("")
    
    # Day of week insights
    if daily_analysis is not None and len(daily_analysis) > 0:
        report.append("BUSIEST DAYS:")
        report.append("-" * 30)
        busiest_days = daily_analysis.nlargest(3, 'transaction_count')
        for _, row in busiest_days.iterrows():
            report.append(f"  {row['day_of_week']}: {row['transaction_count']:.0f} transactions, "
                         f"${row['total_sales']:.2f} sales")
        report.append("")
        
        report.append("SLOWEST DAYS:")
        report.append("-" * 30)
        slowest_days = daily_analysis.nsmallest(3, 'transaction_count')
        for _, row in slowest_days.iterrows():
            report.append(f"  {row['day_of_week']}: {row['transaction_count']:.0f} transactions, "
                         f"${row['total_sales']:.2f} sales")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


# --- Main Execution ---
def main():
    """Main function to run staffing analysis."""
    print("\n--- Starting Staffing Operations Analysis ---\n")
    
    # Load and prepare data
    print("Loading data...")
    df = load_and_prepare_data()
    print(f"Loaded {len(df)} records")
    
    # Analyze hourly patterns
    print("\nAnalyzing hourly patterns...")
    hourly_analysis = analyze_hourly_patterns(df)
    
    # Identify peak and low hours
    print("Identifying peak and low hours...")
    hourly_analysis, peak_hours, low_hours, normal_hours = identify_peak_low_hours(hourly_analysis)
    
    # Analyze day of week patterns
    print("Analyzing day of week patterns...")
    daily_analysis = analyze_day_of_week_patterns(df)
    
    # Generate staffing recommendations
    print("Generating staffing recommendations...")
    hourly_analysis = generate_staffing_recommendations(hourly_analysis)
    
    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(hourly_analysis, daily_analysis)
    
    # Generate and print summary report
    report = generate_summary_report(hourly_analysis, peak_hours, low_hours, daily_analysis)
    print(report)
    
    # Save detailed analysis to CSV
    hourly_analysis.to_csv('staffing_hourly_analysis.csv', index=False)
    print("\nSaved 'staffing_hourly_analysis.csv'")
    
    if daily_analysis is not None:
        daily_analysis.to_csv('staffing_daily_analysis.csv', index=False)
        print("Saved 'staffing_daily_analysis.csv'")
    
    print("\n--- Staffing Analysis Complete ---")
    
    return hourly_analysis, daily_analysis


if __name__ == "__main__":
    main()
