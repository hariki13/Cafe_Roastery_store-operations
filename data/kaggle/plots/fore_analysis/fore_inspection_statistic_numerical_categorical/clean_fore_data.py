#!/usr/bin/env python3
"""
Deep Data Cleaning and Imputation for Coffee Store Location Dataset (fore.csv)
Handles missing values, outliers, data standardization, and quality checks
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
import warnings
warnings.filterwarnings('ignore')

class CoffeeStoreDataCleaner:
    def __init__(self, input_file='fore.csv', output_file='fore_cleaned.csv'):
        """Initialize the data cleaner"""
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        self.original_shape = None
        self.cleaning_report = []
        
    def load_data(self):
        """Load the dataset"""
        print("=" * 80)
        print("📊 COFFEE STORE DATA CLEANING AND IMPUTATION")
        print("=" * 80)
        
        self.df = pd.read_csv(self.input_file)
        self.original_shape = self.df.shape
        
        print(f"\n✅ Data loaded successfully")
        print(f"   Rows: {self.df.shape[0]}")
        print(f"   Columns: {self.df.shape[1]}")
        
        self.cleaning_report.append(f"Original dataset: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
    def analyze_missing_data(self):
        """Analyze missing data patterns"""
        print(f"\n{'=' * 80}")
        print("🔍 MISSING DATA ANALYSIS")
        print("=" * 80)
        
        missing_counts = self.df.isnull().sum()
        missing_percent = (missing_counts / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing_counts.index,
            'Missing_Count': missing_counts.values,
            'Missing_Percent': missing_percent.values
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
        
        if len(missing_df) > 0:
            print("\n📋 Columns with missing values:")
            for _, row in missing_df.iterrows():
                print(f"   • {row['Column']}: {row['Missing_Count']} ({row['Missing_Percent']:.2f}%)")
            
            self.cleaning_report.append(f"Missing values found in {len(missing_df)} columns")
        else:
            print("\n✅ No missing values found!")
            self.cleaning_report.append("No missing values detected")
        
        return missing_df
    
    def clean_text_columns(self):
        """Clean and standardize text columns"""
        print(f"\n{'=' * 80}")
        print("🧹 TEXT DATA CLEANING")
        print("=" * 80)
        
        text_columns = ['OutletLocation', 'OutletCategory', 'StreetAddress1', 'StreetAddress2', 
                       'UrbanVillage', 'Sub-district', 'City', 'Province']
        
        for col in text_columns:
            if col in self.df.columns:
                # Remove leading/trailing whitespace #this line for cleaning text data
                self.df[col] = self.df[col].astype(str).str.strip()
                
                # Replace multiple spaces with single space #this line for standardizing spacing
                self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)
                
                # Replace empty strings with NaN for proper missing data handling
                self.df[col] = self.df[col].replace(['', 'nan', 'None'], np.nan)
                
        print("✅ Text columns cleaned:")
        print(f"   • Removed extra whitespace")
        print(f"   • Standardized spacing")
        print(f"   • Converted empty strings to NaN")
        
        self.cleaning_report.append("Text columns cleaned and standardized")
    
    def clean_time_columns(self):
        """Clean and standardize time columns"""
        print(f"\n{'=' * 80}")
        print("⏰ TIME DATA CLEANING")
        print("=" * 80)
        
        time_columns = ['OpenTime', 'ClosedTime']
        
        for col in time_columns:
            if col in self.df.columns:
                # Standardize time format
                self.df[col] = self.df[col].str.strip()
                
                # Convert to 24-hour format for consistency
                def convert_to_24hr(time_str):
                    try:
                        if pd.isna(time_str):
                            return np.nan
                        time_str = str(time_str).strip()
                        # Parse time #to convert time to 24 hour format
                        time_obj = pd.to_datetime(time_str, format='%I:%M:%S %p', errors='coerce')
                        if pd.isna(time_obj):
                            time_obj = pd.to_datetime(time_str, format='%H:%M:%S', errors='coerce')
                        if pd.notna(time_obj):
                            return time_obj.strftime('%H:%M:%S')
                        return np.nan
                    except Exception as e:
                        return np.nan
                
                self.df[col] = self.df[col].apply(convert_to_24hr)
        
        print("✅ Time columns standardized to 24-hour format")
        self.cleaning_report.append("Time columns converted to 24-hour format")
    
    def clean_rating_columns(self):
        """Clean and validate rating columns"""
        print(f"\n{'=' * 80}")
        print("⭐ RATING DATA CLEANING")
        print("=" * 80)
        
        rating_columns = ['GoogleRating', 'GoFoodRating', 'GrabFoodRating', 'YummyAdvisorRating']
        
        for col in rating_columns:
            if col in self.df.columns:
                # Convert to numeric
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                
                # Validate rating range (0-5)
                invalid_count = ((self.df[col] < 0) | (self.df[col] > 5)).sum()
                if invalid_count > 0:
                    print(f"   ⚠️  {col}: {invalid_count} values outside valid range (0-5)")
                    self.df.loc[(self.df[col] < 0) | (self.df[col] > 5), col] = np.nan
        
        print("✅ Rating columns validated and cleaned")
        self.cleaning_report.append("Rating columns validated (0-5 range)")
    
    def impute_missing_ratings(self):
        """Impute missing rating values using intelligent strategies"""
        print(f"\n{'=' * 80}")
        print("🔧 RATING IMPUTATION")
        print("=" * 80)
        
        rating_columns = ['GoogleRating', 'GoFoodRating', 'GrabFoodRating', 'YummyAdvisorRating']
        
        # Strategy 1: Use mean of other ratings for the same store
        for idx, row in self.df.iterrows():
            available_ratings = []
            for col in rating_columns:
                if col in self.df.columns and pd.notna(row[col]):
                    available_ratings.append(row[col])
            
            if len(available_ratings) > 0:
                mean_rating = np.mean(available_ratings)
                for col in rating_columns:
                    if col in self.df.columns and pd.isna(row[col]):
                        self.df.at[idx, col] = round(mean_rating, 1)
        
        # Strategy 2: Use category mean for remaining missing values
        for col in rating_columns:
            if col in self.df.columns:
                missing_before = self.df[col].isnull().sum()
                if missing_before > 0:
                    # Group by outlet category and impute with category mean
                    category_means = self.df.groupby('OutletCategory')[col].transform('mean')
                    self.df[col].fillna(category_means, inplace=True)
                    
                    # If still missing, use overall mean
                    overall_mean = self.df[col].mean()
                    self.df[col].fillna(overall_mean, inplace=True)
                    
                    missing_after = self.df[col].isnull().sum()
                    imputed = missing_before - missing_after
                    if imputed > 0:
                        print(f"   ✅ {col}: Imputed {imputed} missing values")
        
        self.cleaning_report.append("Missing ratings imputed using multi-strategy approach")
    
    def impute_missing_text(self):
        """Impute missing text values"""
        print(f"\n{'=' * 80}")
        print("🔧 TEXT DATA IMPUTATION")
        print("=" * 80)
        
        # StreetAddress2 - many stores don't have a second address line
        if 'StreetAddress2' in self.df.columns:
            missing_count = self.df['StreetAddress2'].isnull().sum()
            self.df['StreetAddress2'].fillna('N/A', inplace=True)
            if missing_count > 0:
                print(f"   ✅ StreetAddress2: Filled {missing_count} missing values with 'N/A'")
        
        # For other text columns, keep NaN as it indicates truly missing data
        # that should not be fabricated
        
        self.cleaning_report.append("Secondary address field filled with 'N/A' where missing")
    
    def detect_and_handle_outliers(self):
        """Detect and handle outliers in rating data"""
        print(f"\n{'=' * 80}")
        print("📊 OUTLIER DETECTION")
        print("=" * 80)
        
        rating_columns = ['GoogleRating', 'GoFoodRating', 'GrabFoodRating', 'YummyAdvisorRating']
        
        for col in rating_columns:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                
                if outliers > 0:
                    print(f"   ℹ️  {col}: {outliers} outliers detected (kept as valid data)")
        
        print("\n   Note: Outliers in ratings are kept as they represent valid extreme values")
        self.cleaning_report.append("Outlier detection completed - extreme ratings kept as valid")
    
    def add_derived_features(self):
        """Add useful derived features"""
        print(f"\n{'=' * 80}")
        print("✨ FEATURE ENGINEERING")
        print("=" * 80)
        
        # Average Rating across all platforms
        rating_columns = ['GoogleRating', 'GoFoodRating', 'GrabFoodRating', 'YummyAdvisorRating']
        available_ratings = [col for col in rating_columns if col in self.df.columns]
        
        if len(available_ratings) > 0:
            self.df['AverageRating'] = self.df[available_ratings].mean(axis=1).round(2)
            print(f"   ✅ Added 'AverageRating' (mean of all platform ratings)")
        
        # Rating Count (how many platforms have rated)
        self.df['RatingCount'] = self.df[available_ratings].notna().sum(axis=1)
        print(f"   ✅ Added 'RatingCount' (number of rating platforms)")
        
        # Store Type Simplified
        if 'OutletCategory' in self.df.columns:
            self.df['StoreType'] = self.df['OutletCategory'].map({
                'Shopping Mall': 'Mall',
                'CafeStore': 'Standalone',
                'University': 'Institutional'
            })
            print(f"   ✅ Added 'StoreType' (simplified category)")
        
        # Region grouping
        if 'Province' in self.df.columns:
            region_map = {
                'Sumatera Utara': 'Sumatra',
                'Sumatera Barat': 'Sumatra',
                'Sumatera Selatan': 'Sumatra',
                'Lampung': 'Sumatra',
                'Kepulauan Riau': 'Sumatra',
                'Bali': 'Bali-Nusa Tenggara',
                'Sulawesi Selatan': 'Sulawesi',
                'Kalimantan Barat': 'Kalimantan',
                'Kalimantan Selatan': 'Kalimantan',
                'Kalimantan Timur': 'Kalimantan',
                'Yogyakarta': 'Java',
                'Jawa Tengah': 'Java',
                'Jawa Timur': 'Java',
                'Jawa Barat': 'Java'
            }
            self.df['Region'] = self.df['Province'].map(region_map)
            print(f"   ✅ Added 'Region' (geographic grouping)")
        
        self.cleaning_report.append("Derived features created: AverageRating, RatingCount, StoreType, Region")
    
    def validate_postal_codes(self):
        """Validate and clean postal codes"""
        print(f"\n{'=' * 80}")
        print("📮 POSTAL CODE VALIDATION")
        print("=" * 80)
        
        if 'PostalCode' in self.df.columns:
            # Convert to string and remove any non-numeric characters
            self.df['PostalCode'] = self.df['PostalCode'].astype(str).str.replace(r'\D', '', regex=True)
            
            # Indonesian postal codes are 5 digits
            invalid_count = (self.df['PostalCode'].str.len() != 5).sum()
            
            if invalid_count > 0:
                print(f"   ⚠️  Found {invalid_count} invalid postal codes")
                # Pad with leading zeros if needed
                self.df['PostalCode'] = self.df['PostalCode'].str.zfill(5)
            
            print(f"   ✅ Postal codes validated and standardized")
            self.cleaning_report.append("Postal codes validated and standardized to 5 digits")
    
    def generate_data_quality_report(self):
        """Generate comprehensive data quality report"""
        print(f"\n{'=' * 80}")
        print("📋 DATA QUALITY REPORT")
        print("=" * 80)
        
        print(f"\n📊 Dataset Overview:")
        print(f"   • Total Records: {len(self.df)}")
        print(f"   • Total Columns: {len(self.df.columns)}")
        print(f"   • Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        print(f"\n✅ Completeness:")
        completeness = (1 - self.df.isnull().sum() / len(self.df)) * 100
        for col in self.df.columns:
            comp = completeness[col]
            status = "✅" if comp == 100 else "⚠️ " if comp >= 90 else "❌"
            print(f"   {status} {col}: {comp:.1f}%")
        
        print(f"\n📊 Summary Statistics (Ratings):")
        rating_cols = ['GoogleRating', 'GoFoodRating', 'GrabFoodRating', 
                      'YummyAdvisorRating', 'AverageRating']
        for col in rating_cols:
            if col in self.df.columns:
                print(f"   • {col}:")
                print(f"     Mean: {self.df[col].mean():.2f}, Median: {self.df[col].median():.2f}, "
                      f"Std: {self.df[col].std():.2f}")
        
        print(f"\n🏪 Store Distribution:")
        if 'OutletCategory' in self.df.columns:
            print(self.df['OutletCategory'].value_counts().to_string())
        
        print(f"\n🌍 Geographic Distribution:")
        if 'Region' in self.df.columns:
            print(self.df['Region'].value_counts().to_string())
    
    def save_cleaned_data(self):
        """Save cleaned dataset"""
        print(f"\n{'=' * 80}")
        print("💾 SAVING CLEANED DATA")
        print("=" * 80)
        
        self.df.to_csv(self.output_file, index=False)
        print(f"\n✅ Cleaned data saved to: {self.output_file}")
        print(f"   • Rows: {self.df.shape[0]}")
        print(f"   • Columns: {self.df.shape[1]}")
        
        # Save cleaning report
        report_file = self.output_file.replace('.csv', '_report.txt')
        with open(report_file, 'w') as f:
            f.write("COFFEE STORE DATA CLEANING REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for item in self.cleaning_report:
                f.write(f"• {item}\n")
        
        print(f"   • Report saved to: {report_file}")
    
    def run_full_cleaning(self):
        """Execute full cleaning pipeline"""
        try:
            self.load_data()
            self.analyze_missing_data()
            self.clean_text_columns()
            self.clean_time_columns()
            self.validate_postal_codes()
            self.clean_rating_columns()
            self.impute_missing_ratings()
            self.impute_missing_text()
            self.detect_and_handle_outliers()
            self.add_derived_features()
            self.generate_data_quality_report()
            self.save_cleaned_data()
            
            print(f"\n{'=' * 80}")
            print("🎉 DATA CLEANING COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ Error during cleaning: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main execution function"""
    cleaner = CoffeeStoreDataCleaner(
        input_file='fore.csv',
        output_file='fore_cleaned.csv'
    )
    cleaner.run_full_cleaning()


if __name__ == '__main__':
    main()
