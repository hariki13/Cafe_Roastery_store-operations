# --- Coffee Roasting Data Analytics ---
# This module provides data analysis and analytics for coffee roastery operations
# It includes roast profile analysis, quality metrics, and operational insights

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


def generate_sample_roasting_data(num_batches=100):
    """
    Generate sample coffee roasting data for demonstration and testing.
    
    Returns:
        pd.DataFrame: Sample roasting data with batch info, temperatures, times, and quality metrics
    """
    np.random.seed(42)
    
    # Coffee bean origins
    origins = ['Ethiopia', 'Colombia', 'Brazil', 'Guatemala', 'Kenya', 'Indonesia', 'Costa Rica']
    
    # Roast levels
    roast_levels = ['Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark']
    
    # Generate sample data
    data = {
        'batch_id': [f'BATCH-{i:04d}' for i in range(1, num_batches + 1)],
        'roast_date': [datetime(2024, 1, 1) + timedelta(days=i % 365) for i in range(num_batches)],
        'bean_origin': np.random.choice(origins, num_batches),
        'green_bean_weight_kg': np.round(np.random.uniform(5, 25, num_batches), 2),
        'roast_level': np.random.choice(roast_levels, num_batches),
        'charge_temp_celsius': np.round(np.random.uniform(180, 220, num_batches), 1),
        'first_crack_temp_celsius': np.round(np.random.uniform(195, 210, num_batches), 1),
        'first_crack_time_min': np.round(np.random.uniform(8, 12, num_batches), 2),
        'drop_temp_celsius': np.round(np.random.uniform(200, 230, num_batches), 1),
        'total_roast_time_min': np.round(np.random.uniform(10, 18, num_batches), 2),
        'development_time_ratio': np.round(np.random.uniform(0.15, 0.30, num_batches), 3),
        'weight_loss_percent': np.round(np.random.uniform(12, 18, num_batches), 2),
        'agtron_score': np.random.randint(25, 85, num_batches),
        'cupping_score': np.round(np.random.uniform(75, 95, num_batches), 1),
        'roaster_id': np.random.choice(['Roaster-A', 'Roaster-B', 'Roaster-C'], num_batches),
    }
    
    return pd.DataFrame(data)


def clean_roasting_data(df):
    """
    Clean and validate coffee roasting data.
    
    Args:
        df: DataFrame with roasting data
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("\n--- Starting Data Cleaning ---")
    initial_rows = len(df)
    
    # Convert roast_date to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df['roast_date']):
        df['roast_date'] = pd.to_datetime(df['roast_date'], errors='coerce')
    
    # Remove rows with missing critical values
    critical_columns = ['batch_id', 'roast_date', 'bean_origin', 'total_roast_time_min', 'cupping_score']
    df.dropna(subset=critical_columns, inplace=True)
    
    # Remove duplicate batches
    df.drop_duplicates(subset=['batch_id'], inplace=True)
    
    # Validate temperature ranges (reasonable bounds for coffee roasting)
    df = df[(df['charge_temp_celsius'] >= 150) & (df['charge_temp_celsius'] <= 250)]
    df = df[(df['drop_temp_celsius'] >= 180) & (df['drop_temp_celsius'] <= 260)]
    
    # Validate time ranges
    df = df[(df['total_roast_time_min'] >= 5) & (df['total_roast_time_min'] <= 25)]
    
    # Validate cupping scores (SCA scale is 0-100)
    df = df[(df['cupping_score'] >= 0) & (df['cupping_score'] <= 100)]
    
    final_rows = len(df)
    print(f"Removed {initial_rows - final_rows} invalid or duplicate rows.")
    print(f"Remaining rows: {final_rows}")
    
    return df


def perform_roasting_analytics(df):
    """
    Perform descriptive analytics on coffee roasting data.
    
    Args:
        df: Cleaned DataFrame with roasting data
        
    Returns:
        dict: Analytics results
    """
    print("\n--- Performing Roasting Analytics ---")
    
    analytics = {}
    
    # Overall statistics
    analytics['total_batches'] = len(df)
    analytics['total_green_beans_kg'] = df['green_bean_weight_kg'].sum()
    analytics['avg_cupping_score'] = df['cupping_score'].mean()
    analytics['avg_roast_time_min'] = df['total_roast_time_min'].mean()
    analytics['avg_weight_loss_percent'] = df['weight_loss_percent'].mean()
    
    print(f"\n1. Total Batches Roasted: {analytics['total_batches']}")
    print(f"2. Total Green Beans Processed: {analytics['total_green_beans_kg']:.2f} kg")
    print(f"3. Average Cupping Score: {analytics['avg_cupping_score']:.2f}")
    print(f"4. Average Roast Time: {analytics['avg_roast_time_min']:.2f} min")
    print(f"5. Average Weight Loss: {analytics['avg_weight_loss_percent']:.2f}%")
    
    # Analysis by origin
    origin_analysis = df.groupby('bean_origin').agg({
        'cupping_score': ['mean', 'std', 'count'],
        'total_roast_time_min': 'mean',
        'weight_loss_percent': 'mean'
    }).round(2)
    origin_analysis.columns = ['avg_score', 'score_std', 'batch_count', 'avg_roast_time', 'avg_weight_loss']
    analytics['by_origin'] = origin_analysis.sort_values('avg_score', ascending=False)
    
    print("\n6. Quality Metrics by Bean Origin:")
    print(analytics['by_origin'])
    
    # Analysis by roast level
    roast_level_analysis = df.groupby('roast_level').agg({
        'cupping_score': 'mean',
        'agtron_score': 'mean',
        'weight_loss_percent': 'mean',
        'batch_id': 'count'
    }).round(2)
    roast_level_analysis.columns = ['avg_cupping_score', 'avg_agtron', 'avg_weight_loss', 'batch_count']
    analytics['by_roast_level'] = roast_level_analysis
    
    print("\n7. Analysis by Roast Level:")
    print(analytics['by_roast_level'])
    
    # Analysis by roaster
    roaster_analysis = df.groupby('roaster_id').agg({
        'cupping_score': ['mean', 'count'],
        'total_roast_time_min': 'mean'
    }).round(2)
    roaster_analysis.columns = ['avg_score', 'batch_count', 'avg_roast_time']
    analytics['by_roaster'] = roaster_analysis
    
    print("\n8. Performance by Roaster:")
    print(analytics['by_roaster'])
    
    # Quality distribution
    analytics['specialty_grade_count'] = len(df[df['cupping_score'] >= 80])
    analytics['specialty_grade_percent'] = (analytics['specialty_grade_count'] / len(df)) * 100
    
    print(f"\n9. Specialty Grade Batches (≥80 points): {analytics['specialty_grade_count']} ({analytics['specialty_grade_percent']:.1f}%)")
    
    return analytics


def create_roasting_visualizations(df, save_plots=True):
    """
    Create visualizations for coffee roasting analytics.
    
    Args:
        df: DataFrame with roasting data
        save_plots: Whether to save plots to files
    """
    print("\n--- Creating Visualizations ---")
    sns.set_style('whitegrid')
    
    # 1. Cupping Score Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='cupping_score', bins=20, kde=True, color='brown')
    plt.axvline(x=80, color='green', linestyle='--', label='Specialty Threshold (80)')
    plt.title('Distribution of Cupping Scores', fontsize=16)
    plt.xlabel('Cupping Score', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend()
    plt.tight_layout()
    if save_plots:
        plt.savefig('cupping_score_distribution.png')
        print("1. Saved 'cupping_score_distribution.png'")
    
    # 2. Average Cupping Score by Origin
    plt.figure(figsize=(12, 6))
    origin_scores = df.groupby('bean_origin')['cupping_score'].mean().sort_values(ascending=True).reset_index()
    sns.barplot(data=origin_scores, x='cupping_score', y='bean_origin', hue='bean_origin', 
                palette='YlOrBr', legend=False)
    plt.title('Average Cupping Score by Bean Origin', fontsize=16)
    plt.xlabel('Average Cupping Score', fontsize=12)
    plt.ylabel('Bean Origin', fontsize=12)
    plt.tight_layout()
    if save_plots:
        plt.savefig('cupping_score_by_origin.png')
        print("2. Saved 'cupping_score_by_origin.png'")
    
    # 3. Roast Time vs Cupping Score
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='total_roast_time_min', y='cupping_score', 
                    hue='roast_level', style='roast_level', s=100, alpha=0.7)
    plt.title('Roast Time vs Cupping Score', fontsize=16)
    plt.xlabel('Total Roast Time (min)', fontsize=12)
    plt.ylabel('Cupping Score', fontsize=12)
    plt.legend(title='Roast Level', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    if save_plots:
        plt.savefig('roast_time_vs_quality.png')
        print("3. Saved 'roast_time_vs_quality.png'")
    
    # 4. Weight Loss Distribution by Roast Level
    plt.figure(figsize=(12, 6))
    roast_order = ['Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark']
    sns.boxplot(data=df, x='roast_level', y='weight_loss_percent', 
                order=roast_order, hue='roast_level', palette='Oranges', legend=False)
    plt.title('Weight Loss Distribution by Roast Level', fontsize=16)
    plt.xlabel('Roast Level', fontsize=12)
    plt.ylabel('Weight Loss (%)', fontsize=12)
    plt.tight_layout()
    if save_plots:
        plt.savefig('weight_loss_by_roast_level.png')
        print("4. Saved 'weight_loss_by_roast_level.png'")
    
    # 5. Development Time Ratio Analysis
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='development_time_ratio', y='cupping_score', 
                    hue='bean_origin', s=100, alpha=0.7)
    plt.title('Development Time Ratio vs Cupping Score', fontsize=16)
    plt.xlabel('Development Time Ratio', fontsize=12)
    plt.ylabel('Cupping Score', fontsize=12)
    plt.axvline(x=0.20, color='red', linestyle='--', alpha=0.5, label='Optimal Range')
    plt.axvline(x=0.25, color='red', linestyle='--', alpha=0.5)
    plt.legend(title='Bean Origin', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    if save_plots:
        plt.savefig('dtr_vs_quality.png')
        print("5. Saved 'dtr_vs_quality.png'")
    
    # 6. Monthly Production Trend
    df_copy = df.copy()
    df_copy['month'] = df_copy['roast_date'].dt.to_period('M')
    monthly_production = df_copy.groupby('month').agg({
        'green_bean_weight_kg': 'sum',
        'cupping_score': 'mean'
    })
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax1.bar(range(len(monthly_production)), monthly_production['green_bean_weight_kg'], 
            color='brown', alpha=0.7, label='Production (kg)')
    ax1.set_xlabel('Month', fontsize=12)
    ax1.set_ylabel('Green Bean Weight (kg)', fontsize=12, color='brown')
    ax1.tick_params(axis='y', labelcolor='brown')
    
    ax2 = ax1.twinx()
    ax2.plot(range(len(monthly_production)), monthly_production['cupping_score'], 
             color='green', marker='o', linewidth=2, label='Avg Cupping Score')
    ax2.set_ylabel('Average Cupping Score', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title('Monthly Production Volume and Quality', fontsize=16)
    fig.tight_layout()
    if save_plots:
        plt.savefig('monthly_production_trend.png')
        print("6. Saved 'monthly_production_trend.png'")
    
    # 7. Heatmap: Roast Parameters Correlation
    plt.figure(figsize=(12, 10))
    numeric_cols = ['green_bean_weight_kg', 'charge_temp_celsius', 'first_crack_temp_celsius',
                   'first_crack_time_min', 'drop_temp_celsius', 'total_roast_time_min',
                   'development_time_ratio', 'weight_loss_percent', 'agtron_score', 'cupping_score']
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu', center=0, 
                fmt='.2f', square=True, linewidths=0.5)
    plt.title('Correlation Matrix: Roasting Parameters', fontsize=16)
    plt.tight_layout()
    if save_plots:
        plt.savefig('roasting_parameters_correlation.png')
        print("7. Saved 'roasting_parameters_correlation.png'")
    
    # Close all figures to prevent memory leaks
    plt.close('all')


def generate_roasting_report(df, analytics, output_file='roasting_report.csv'):
    """
    Generate a summary report of roasting operations.
    
    Args:
        df: DataFrame with roasting data
        analytics: Analytics results dictionary
        output_file: Output CSV filename
    """
    print(f"\n--- Generating Report ---")
    
    # Export cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data exported to '{output_file}'")
    
    # Print summary
    print("\n=== COFFEE ROASTING OPERATIONS SUMMARY ===")
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTotal Batches Analyzed: {analytics['total_batches']}")
    print(f"Total Green Beans Processed: {analytics['total_green_beans_kg']:.2f} kg")
    print(f"Average Cupping Score: {analytics['avg_cupping_score']:.2f}")
    print(f"Specialty Grade Rate: {analytics['specialty_grade_percent']:.1f}%")
    print("\nTop Performing Origins:")
    print(analytics['by_origin'].head(3))
    print("=" * 50)


def main():
    """
    Main function to run coffee roasting analytics pipeline.
    """
    print("=" * 60)
    print("  COFFEE ROASTERY OPERATIONS ANALYTICS")
    print("=" * 60)
    
    # Step 1: Generate or load roasting data
    print("\n--- Step 1: Loading Data ---")
    # For demonstration, generate sample data
    # In production, replace with: df = pd.read_csv('roasting_data.csv')
    df = generate_sample_roasting_data(num_batches=200)
    print(f"Loaded {len(df)} roasting batch records")
    print(f"\nData Preview:")
    print(df.head())
    print(f"\nData Info:")
    print(df.info())
    
    # Step 2: Clean the data
    df_clean = clean_roasting_data(df)
    
    # Step 3: Perform analytics
    analytics = perform_roasting_analytics(df_clean)
    
    # Step 4: Create visualizations
    create_roasting_visualizations(df_clean, save_plots=True)
    
    # Step 5: Generate report
    generate_roasting_report(df_clean, analytics, 'coffee_roasting_data_cleaned.csv')
    
    print("\n--- Analysis Complete ---")
    print("Generated visualization files:")
    print("  - cupping_score_distribution.png")
    print("  - cupping_score_by_origin.png")
    print("  - roast_time_vs_quality.png")
    print("  - weight_loss_by_roast_level.png")
    print("  - dtr_vs_quality.png")
    print("  - monthly_production_trend.png")
    print("  - roasting_parameters_correlation.png")


if __name__ == "__main__":
    main()
