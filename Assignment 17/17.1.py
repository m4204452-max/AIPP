import pandas as pd
import re
from datetime import datetime

# Common English stopwords
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
    'have', 'had', 'what', 'said', 'each', 'which', 'their', 'time',
    'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
    'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more',
    'very', 'after', 'words', 'long', 'than', 'first', 'been', 'call',
    'who', 'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get',
    'come', 'made', 'may', 'part'
}

def clean_text(text):
    """
    Remove stopwords, punctuation, and special symbols from text.
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and punctuation, but keep spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in STOPWORDS and len(word) > 1]
    
    return ' '.join(words)

def handle_missing_values(df):
    """
    Handle missing values in likes and shares columns.
    """
    # Fill missing values with median (more robust than mean for engagement metrics)
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce')
    df['shares'] = pd.to_numeric(df['shares'], errors='coerce')
    
    # Fill missing values with median of the respective column
    df['likes'].fillna(df['likes'].median(), inplace=True)
    df['shares'].fillna(df['shares'].median(), inplace=True)
    
    # Convert to int for cleaner output
    df['likes'] = df['likes'].astype(int)
    df['shares'] = df['shares'].astype(int)
    
    return df

def extract_datetime_features(df):
    """
    Convert timestamp to datetime and extract hour and weekday features.
    """
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract hour (0-23)
    df['hour'] = df['timestamp'].dt.hour
    
    # Extract weekday (0=Monday, 6=Sunday)
    df['weekday'] = df['timestamp'].dt.dayofweek
    
    # Add weekday name for better readability
    df['weekday_name'] = df['timestamp'].dt.day_name()
    
    return df

def detect_and_remove_duplicates(df):
    """
    Detect and remove spam/duplicate posts based on post_text similarity.
    """
    # Find duplicate posts based on cleaned text
    # Keep the first occurrence (usually the earliest or most engaged)
    duplicates_mask = df.duplicated(subset=['post_text_cleaned'], keep='first')
    
    # Count duplicates before removal
    num_duplicates = duplicates_mask.sum()
    print(f"Found {num_duplicates} duplicate posts to remove.")
    
    # Remove duplicates
    df_cleaned = df[~duplicates_mask].copy()
    
    return df_cleaned

def main():
    """
    Main function to clean social media dataset.
    """
    # Load the dataset
    print("Loading social media dataset...")
    df = pd.read_csv('social_media (1).csv')
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original columns: {df.columns.tolist()}\n")
    
    # Step 1: Clean post text (remove stopwords, punctuation, special symbols)
    print("Step 1: Cleaning post text...")
    df['post_text_cleaned'] = df['post_text'].apply(clean_text)
    
    # Step 2: Handle missing values in likes and shares
    print("Step 2: Handling missing values in likes and shares...")
    df = handle_missing_values(df)
    
    # Step 3: Convert timestamp and extract features
    print("Step 3: Extracting datetime features...")
    df = extract_datetime_features(df)
    
    # Step 4: Detect and remove duplicates/spam
    print("Step 4: Detecting and removing duplicate posts...")
    df_cleaned = detect_and_remove_duplicates(df)
    
    # Reorder columns for better readability
    column_order = ['post_id', 'user', 'post_text', 'post_text_cleaned', 
                    'likes', 'shares', 'timestamp', 'hour', 'weekday', 'weekday_name']
    df_cleaned = df_cleaned[column_order]
    
    print(f"\nCleaned dataset shape: {df_cleaned.shape}")
    print(f"\nCleaned dataset preview:")
    print(df_cleaned.head(10))
    
    # Save cleaned dataset
    output_file = 'social_media_cleaned.csv'
    df_cleaned.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to: {output_file}")
    
    # Display summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total posts: {len(df_cleaned)}")
    print(f"Average likes: {df_cleaned['likes'].mean():.2f}")
    print(f"Average shares: {df_cleaned['shares'].mean():.2f}")
    print(f"\nPosts by weekday:")
    print(df_cleaned['weekday_name'].value_counts().sort_index())
    print(f"\nPosts by hour:")
    print(df_cleaned['hour'].value_counts().sort_index())
    
    return df_cleaned

if __name__ == "__main__":
    cleaned_data = main()

