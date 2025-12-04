import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime

def handle_missing_values(df):
    """
    Handle missing values using forward fill.
    Forward fill carries the last known value forward, which is appropriate
    for time-series sensor data.
    """
    # Convert to numeric
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    
    # Sort by timestamp and sensor_id to ensure proper order
    df = df.sort_values(['timestamp', 'sensor_id']).reset_index(drop=True)
    
    # Forward fill missing values (grouped by sensor_id to maintain sensor-specific continuity)
    df['temperature'] = df.groupby('sensor_id')['temperature'].ffill()
    df['humidity'] = df.groupby('sensor_id')['humidity'].ffill()
    
    # If still missing (e.g., first value for a sensor), use backward fill
    df['temperature'] = df.groupby('sensor_id')['temperature'].bfill()
    df['humidity'] = df.groupby('sensor_id')['humidity'].bfill()
    
    # If still missing, fill with sensor-specific mean
    df['temperature'] = df.groupby('sensor_id')['temperature'].transform(
        lambda x: x.fillna(x.mean())
    )
    df['humidity'] = df.groupby('sensor_id')['humidity'].transform(
        lambda x: x.fillna(x.mean())
    )
    
    return df

def remove_sensor_drift(df, window_size=5):
    """
    Remove sensor drift by applying rolling mean.
    Rolling mean smooths out short-term fluctuations and drift.
    """
    # Sort by timestamp and sensor_id
    df = df.sort_values(['timestamp', 'sensor_id']).reset_index(drop=True)
    
    # Apply rolling mean grouped by sensor_id
    # This ensures each sensor's drift is handled independently
    df['temperature_rolling'] = df.groupby('sensor_id')['temperature'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1, center=True).mean()
    )
    df['humidity_rolling'] = df.groupby('sensor_id')['humidity'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1, center=True).mean()
    )
    
    # Replace original values with smoothed values
    df['temperature'] = df['temperature_rolling']
    df['humidity'] = df['humidity_rolling']
    
    # Drop temporary columns
    df.drop(['temperature_rolling', 'humidity_rolling'], axis=1, inplace=True)
    
    return df

def normalize_readings(df):
    """
    Normalize temperature and humidity readings using standard scaling (z-score normalization).
    Standard scaling: (x - mean) / std
    """
    # Create a copy to avoid modifying original data during scaling
    scaler_temp = StandardScaler()
    scaler_humidity = StandardScaler()
    
    # Fit and transform temperature
    df['temperature_normalized'] = scaler_temp.fit_transform(df[['temperature']])
    
    # Fit and transform humidity
    df['humidity_normalized'] = scaler_humidity.fit_transform(df[['humidity']])
    
    # Store scaling parameters for reference
    print(f"\nTemperature Scaling:")
    print(f"  Mean: {scaler_temp.mean_[0]:.4f}, Std: {scaler_temp.scale_[0]:.4f}")
    print(f"\nHumidity Scaling:")
    print(f"  Mean: {scaler_humidity.mean_[0]:.4f}, Std: {scaler_humidity.scale_[0]:.4f}")
    
    return df, scaler_temp, scaler_humidity

def encode_sensor_ids(df):
    """
    Encode categorical sensor IDs using LabelEncoder.
    This converts categorical sensor IDs to numerical values.
    """
    # Create label encoder
    label_encoder = LabelEncoder()
    
    # Fit and transform sensor_id
    df['sensor_id_encoded'] = label_encoder.fit_transform(df['sensor_id'])
    
    # Display encoding mapping
    encoding_map = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    print(f"\nSensor ID Encoding:")
    for sensor_id, encoded_value in encoding_map.items():
        print(f"  {sensor_id} -> {encoded_value}")
    
    return df, label_encoder

def main():
    """
    Main function to preprocess IoT sensor dataset.
    """
    # Load the dataset
    print("Loading IoT sensor dataset...")
    df = pd.read_csv('iot_sensor.csv')
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original columns: {df.columns.tolist()}\n")
    
    # Check initial missing values
    print("Initial missing values:")
    print(f"  temperature: {df['temperature'].isna().sum()}")
    print(f"  humidity: {df['humidity'].isna().sum()}\n")
    
    # Step 1: Handle missing values using forward fill
    print("Step 1: Handling missing values using forward fill...")
    df = handle_missing_values(df)
    
    print(f"Missing values after handling:")
    print(f"  temperature: {df['temperature'].isna().sum()}")
    print(f"  humidity: {df['humidity'].isna().sum()}\n")
    
    # Step 2: Remove sensor drift using rolling mean
    print("Step 2: Removing sensor drift using rolling mean (window=5)...")
    df = remove_sensor_drift(df, window_size=5)
    
    # Step 3: Normalize readings using standard scaling
    print("Step 3: Normalizing readings using standard scaling...")
    df, scaler_temp, scaler_humidity = normalize_readings(df)
    
    # Step 4: Encode categorical sensor IDs
    print("Step 4: Encoding categorical sensor IDs...")
    df, label_encoder = encode_sensor_ids(df)
    
    # Reorder columns for better readability
    column_order = ['timestamp', 'sensor_id', 'sensor_id_encoded', 
                    'temperature', 'humidity',
                    'temperature_normalized', 'humidity_normalized']
    df = df[column_order]
    
    # Sort by timestamp for final output
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    print(f"\nPreprocessed dataset shape: {df.shape}")
    print(f"\nPreprocessed dataset preview:")
    print(df.head(15))
    print("\n...")
    print(df.tail(15))
    
    # Save preprocessed dataset
    output_file = 'iot_sensor_preprocessed.csv'
    df.to_csv(output_file, index=False)
    print(f"\nPreprocessed dataset saved to: {output_file}")
    
    # Display summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total records: {len(df)}")
    print(f"Unique sensors: {df['sensor_id'].nunique()}")
    print(f"Sensors: {df['sensor_id'].unique().tolist()}")
    
    print(f"\nTemperature Statistics (original):")
    print(f"  Mean: {df['temperature'].mean():.2f}")
    print(f"  Median: {df['temperature'].median():.2f}")
    print(f"  Std Dev: {df['temperature'].std():.2f}")
    print(f"  Min: {df['temperature'].min():.2f}")
    print(f"  Max: {df['temperature'].max():.2f}")
    
    print(f"\nHumidity Statistics (original):")
    print(f"  Mean: {df['humidity'].mean():.2f}")
    print(f"  Median: {df['humidity'].median():.2f}")
    print(f"  Std Dev: {df['humidity'].std():.2f}")
    print(f"  Min: {df['humidity'].min():.2f}")
    print(f"  Max: {df['humidity'].max():.2f}")
    
    print(f"\nNormalized Statistics:")
    print(f"  Temperature (normalized) - Mean: {df['temperature_normalized'].mean():.4f}, Std: {df['temperature_normalized'].std():.4f}")
    print(f"  Humidity (normalized) - Mean: {df['humidity_normalized'].mean():.4f}, Std: {df['humidity_normalized'].std():.4f}")
    
    print(f"\nSensor Distribution:")
    print(df['sensor_id'].value_counts().sort_index())
    
    return df

if __name__ == "__main__":
    preprocessed_data = main()

