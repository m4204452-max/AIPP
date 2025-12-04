import pandas as pd
import numpy as np
from datetime import datetime

def handle_missing_values(df):
    """
    Handle missing values in closing_price and volume columns.
    For time-series data, forward fill is often appropriate, 
    but we can also use interpolation or median.
    """
    # Convert to numeric
    df['closing_price'] = pd.to_numeric(df['closing_price'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    
    # Sort by date to ensure proper time-series order
    df = df.sort_values('date').reset_index(drop=True)
    
    # For closing_price: use forward fill (carry last known price forward)
    # This is common in financial data as prices don't change on non-trading days
    df['closing_price'] = df['closing_price'].ffill()
    
    # If still missing (e.g., first value), use backward fill
    df['closing_price'] = df['closing_price'].bfill()
    
    # For volume: use median of the column (more robust than mean)
    volume_median = df['volume'].median()
    df['volume'].fillna(volume_median, inplace=True)
    
    # Convert to appropriate types
    df['closing_price'] = df['closing_price'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    return df

def create_lag_features(df):
    """
    Create lag features: 1-day and 7-day returns.
    Returns are calculated as: (price_today - price_lag) / price_lag
    """
    # Ensure data is sorted by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Calculate 1-day return: (price_today - price_yesterday) / price_yesterday
    df['price_lag_1'] = df['closing_price'].shift(1)
    df['return_1day'] = (df['closing_price'] - df['price_lag_1']) / df['price_lag_1']
    
    # Calculate 7-day return: (price_today - price_7days_ago) / price_7days_ago
    df['price_lag_7'] = df['closing_price'].shift(7)
    df['return_7day'] = (df['closing_price'] - df['price_lag_7']) / df['price_lag_7']
    
    # Drop intermediate lag columns (keep only returns)
    df.drop(['price_lag_1', 'price_lag_7'], axis=1, inplace=True)
    
    return df

def normalize_volume(df):
    """
    Normalize volume column using log-scaling.
    Log transformation helps with skewed distributions common in volume data.
    """
    # Add small constant to avoid log(0) issues
    df['volume_log'] = np.log1p(df['volume'])  # log1p = log(1 + x), handles zeros better
    
    return df

def detect_outliers_iqr(df, column='closing_price'):
    """
    Detect outliers in closing_price using Interquartile Range (IQR) method.
    Outliers are values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    """
    # Calculate quartiles
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identify outliers
    df['is_outlier'] = (df[column] < lower_bound) | (df[column] > upper_bound)
    
    # Count outliers
    num_outliers = df['is_outlier'].sum()
    
    print(f"\nOutlier Detection (IQR Method) for {column}:")
    print(f"Q1 (25th percentile): {Q1:.2f}")
    print(f"Q3 (75th percentile): {Q3:.2f}")
    print(f"IQR: {IQR:.2f}")
    print(f"Lower bound: {lower_bound:.2f}")
    print(f"Upper bound: {upper_bound:.2f}")
    print(f"Number of outliers detected: {num_outliers}")
    
    if num_outliers > 0:
        print(f"\nOutlier values:")
        outliers = df[df['is_outlier'] == True][['date', column]]
        print(outliers.to_string(index=False))
    
    return df

def main():
    """
    Main function to preprocess financial dataset.
    """
    # Load the dataset
    print("Loading financial dataset...")
    df = pd.read_csv('financial_data.csv')
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original columns: {df.columns.tolist()}\n")
    
    # Check initial missing values
    print("Initial missing values:")
    print(f"  closing_price: {df['closing_price'].isna().sum()}")
    print(f"  volume: {df['volume'].isna().sum()}\n")
    
    # Step 1: Handle missing values
    print("Step 1: Handling missing values...")
    df = handle_missing_values(df)
    
    print(f"Missing values after handling:")
    print(f"  closing_price: {df['closing_price'].isna().sum()}")
    print(f"  volume: {df['volume'].isna().sum()}\n")
    
    # Step 2: Create lag features (1-day and 7-day returns)
    print("Step 2: Creating lag features (1-day and 7-day returns)...")
    df = create_lag_features(df)
    
    # Step 3: Normalize volume using log-scaling
    print("Step 3: Normalizing volume using log-scaling...")
    df = normalize_volume(df)
    
    # Step 4: Detect outliers in closing_price using IQR method
    print("Step 4: Detecting outliers in closing_price using IQR method...")
    df = detect_outliers_iqr(df, column='closing_price')
    
    # Reorder columns for better readability
    column_order = ['date', 'closing_price', 'volume', 'volume_log', 
                    'return_1day', 'return_7day', 'is_outlier']
    df = df[column_order]
    
    print(f"\nPreprocessed dataset shape: {df.shape}")
    print(f"\nPreprocessed dataset preview:")
    print(df.head(10))
    print("\n...")
    print(df.tail(10))
    
    # Save preprocessed dataset
    output_file = 'financial_data_preprocessed.csv'
    df.to_csv(output_file, index=False)
    print(f"\nPreprocessed dataset saved to: {output_file}")
    
    # Display summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total records: {len(df)}")
    print(f"\nClosing Price Statistics:")
    print(f"  Mean: {df['closing_price'].mean():.2f}")
    print(f"  Median: {df['closing_price'].median():.2f}")
    print(f"  Std Dev: {df['closing_price'].std():.2f}")
    print(f"  Min: {df['closing_price'].min():.2f}")
    print(f"  Max: {df['closing_price'].max():.2f}")
    
    print(f"\nVolume Statistics:")
    print(f"  Mean: {df['volume'].mean():.2f}")
    print(f"  Median: {df['volume'].median():.2f}")
    print(f"  Std Dev: {df['volume'].std():.2f}")
    
    print(f"\nReturn Statistics:")
    print(f"  1-day return - Mean: {df['return_1day'].mean():.4f}, Std: {df['return_1day'].std():.4f}")
    print(f"  7-day return - Mean: {df['return_7day'].mean():.4f}, Std: {df['return_7day'].std():.4f}")
    
    return df

if __name__ == "__main__":
    preprocessed_data = main()

