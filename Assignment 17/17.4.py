"""
Movie Reviews Data Cleaning and Preprocessing
=============================================

This script performs comprehensive cleaning and preprocessing of movie reviews data:
1. Standardizes review text (lowercase, remove HTML tags)
2. Tokenizes and encodes reviews using TF-IDF
3. Handles missing ratings by filling with median
4. Normalizes ratings from 0-10 to 0-1 scale
5. Generates before vs after summary report
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

# ============================================================================
# STEP 1: Standardize Review Text
# ============================================================================

def standardize_text(text):
    """
    Standardize review text by:
    - Converting to lowercase
    - Removing HTML tags
    - Removing extra whitespace
    
    Args:
        text (str): Raw review text
        
    Returns:
        str: Standardized review text
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def test_standardize_text():
    """
    Test cases for text standardization.
    """
    print("\n=== Testing Text Standardization ===")
    
    # Test Case 1: HTML tag removal
    test1_input = "<p>Amazing movie!</p>"
    test1_expected = "amazing movie!"
    test1_result = standardize_text(test1_input)
    assert test1_result == test1_expected, f"Test 1 failed: Expected '{test1_expected}', got '{test1_result}'"
    print("[PASS] Test 1: HTML tag removal")
    
    # Test Case 2: Lowercase conversion
    test2_input = "TERRIBLE Acting & Plot!!!"
    test2_expected = "terrible acting & plot!!!"
    test2_result = standardize_text(test2_input)
    assert test2_result == test2_expected, f"Test 2 failed: Expected '{test2_expected}', got '{test2_result}'"
    print("[PASS] Test 2: Lowercase conversion")
    
    # Test Case 3: Whitespace normalization
    test3_input = "  Multiple   spaces   here  "
    test3_expected = "multiple spaces here"
    test3_result = standardize_text(test3_input)
    assert test3_result == test3_expected, f"Test 3 failed: Expected '{test3_expected}', got '{test3_result}'"
    print("[PASS] Test 3: Whitespace normalization")
    
    # Test Case 4: Empty/NaN handling
    test4_input = None
    test4_result = standardize_text(test4_input)
    assert test4_result == '', f"Test 4 failed: Expected empty string, got '{test4_result}'"
    print("[PASS] Test 4: Empty/NaN handling")
    
    print("All text standardization tests passed!\n")

# ============================================================================
# STEP 2: Tokenize and Encode Reviews using TF-IDF
# ============================================================================

def tokenize_and_encode_tfidf(df, text_column='review_text_standardized', max_features=100):
    """
    Tokenize and encode reviews using TF-IDF vectorization.
    
    Args:
        df (DataFrame): DataFrame with standardized text
        text_column (str): Name of the text column to encode
        max_features (int): Maximum number of features for TF-IDF
        
    Returns:
        DataFrame: Original DataFrame with TF-IDF features added
        TfidfVectorizer: Fitted vectorizer for potential future use
    """
    # Initialize TF-IDF vectorizer
    # max_features limits vocabulary size, min_df filters rare words
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        min_df=1,  # Minimum document frequency
        stop_words='english',  # Remove common English stopwords
        ngram_range=(1, 2)  # Include unigrams and bigrams
    )
    
    # Fit and transform the text data
    tfidf_matrix = vectorizer.fit_transform(df[text_column].fillna(''))
    
    # Convert to DataFrame
    feature_names = [f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=feature_names,
        index=df.index
    )
    
    # Combine with original dataframe
    df_encoded = pd.concat([df.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)
    
    return df_encoded, vectorizer

def test_tokenize_and_encode():
    """
    Test cases for TF-IDF encoding.
    """
    print("\n=== Testing TF-IDF Encoding ===")
    
    # Create test data
    test_df = pd.DataFrame({
        'review_text_standardized': [
            'amazing movie',
            'terrible acting',
            'amazing movie'
        ]
    })
    
    # Test Case 1: TF-IDF creates features
    test_df_encoded, vectorizer = tokenize_and_encode_tfidf(test_df, max_features=10)
    assert 'tfidf_0' in test_df_encoded.columns, "Test 1 failed: TF-IDF features not created"
    print("[PASS] Test 1: TF-IDF features created")
    
    # Test Case 2: Number of features matches max_features
    tfidf_cols = [col for col in test_df_encoded.columns if col.startswith('tfidf_')]
    assert len(tfidf_cols) <= 10, f"Test 2 failed: Expected <= 10 features, got {len(tfidf_cols)}"
    print("[PASS] Test 2: Feature count within limit")
    
    # Test Case 3: TF-IDF values are between 0 and 1
    tfidf_values = test_df_encoded[tfidf_cols].values
    assert (tfidf_values >= 0).all() and (tfidf_values <= 1).all(), \
        "Test 3 failed: TF-IDF values not in [0, 1] range"
    print("[PASS] Test 3: TF-IDF values in valid range")
    
    print("All TF-IDF encoding tests passed!\n")

# ============================================================================
# STEP 3: Handle Missing Ratings
# ============================================================================

def handle_missing_ratings(df, rating_column='rating'):
    """
    Handle missing ratings by filling with median rating.
    
    Args:
        df (DataFrame): DataFrame with rating column
        rating_column (str): Name of the rating column
        
    Returns:
        DataFrame: DataFrame with missing ratings filled
        float: Median rating used for filling
    """
    # Convert to numeric
    df[rating_column] = pd.to_numeric(df[rating_column], errors='coerce')
    
    # Calculate median (excluding NaN)
    median_rating = df[rating_column].median()
    
    # Fill missing values with median
    df[rating_column] = df[rating_column].fillna(median_rating)
    
    return df, median_rating

def test_handle_missing_ratings():
    """
    Test cases for missing rating handling.
    """
    print("\n=== Testing Missing Rating Handling ===")
    
    # Test Case 1: Missing values filled with median
    test_df = pd.DataFrame({
        'rating': [8.0, 2.0, np.nan, 5.0, 10.0]
    })
    test_df_filled, median = handle_missing_ratings(test_df)
    assert test_df_filled['rating'].isna().sum() == 0, "Test 1 failed: Missing values not filled"
    print("[PASS] Test 1: Missing values filled")
    
    # Test Case 2: Median calculation is correct
    expected_median = 6.5  # Median of [2.0, 5.0, 8.0, 10.0]
    assert median == expected_median, f"Test 2 failed: Expected median {expected_median}, got {median}"
    print("[PASS] Test 2: Median calculation correct")
    
    # Test Case 3: Filled values match median
    filled_value = test_df_filled[test_df_filled['rating'].notna()].iloc[2]['rating']
    assert filled_value == median, f"Test 3 failed: Filled value {filled_value} != median {median}"
    print("[PASS] Test 3: Filled values match median")
    
    print("All missing rating handling tests passed!\n")

# ============================================================================
# STEP 4: Normalize Ratings
# ============================================================================

def normalize_ratings(df, rating_column='rating', min_original=0, max_original=10, 
                      min_target=0, max_target=1):
    """
    Normalize ratings from original scale (0-10) to target scale (0-1).
    
    Formula: normalized = (rating - min_original) / (max_original - min_original) * (max_target - min_target) + min_target
    
    Args:
        df (DataFrame): DataFrame with rating column
        rating_column (str): Name of the rating column
        min_original (float): Minimum value in original scale
        max_original (float): Maximum value in original scale
        min_target (float): Minimum value in target scale
        max_target (float): Maximum value in target scale
        
    Returns:
        DataFrame: DataFrame with normalized ratings
    """
    # Create normalized column
    normalized_column = f'{rating_column}_normalized'
    
    # Apply min-max normalization
    df[normalized_column] = (df[rating_column] - min_original) / (max_original - min_original) * \
                           (max_target - min_target) + min_target
    
    return df

def test_normalize_ratings():
    """
    Test cases for rating normalization.
    """
    print("\n=== Testing Rating Normalization ===")
    
    # Test Case 1: Minimum value (0) normalizes to 0
    test_df = pd.DataFrame({'rating': [0.0, 5.0, 10.0]})
    test_df = normalize_ratings(test_df)
    assert abs(test_df['rating_normalized'].iloc[0] - 0.0) < 0.001, \
        "Test 1 failed: Minimum value not normalized to 0"
    print("[PASS] Test 1: Minimum value normalized to 0")
    
    # Test Case 2: Maximum value (10) normalizes to 1
    assert abs(test_df['rating_normalized'].iloc[2] - 1.0) < 0.001, \
        "Test 2 failed: Maximum value not normalized to 1"
    print("[PASS] Test 2: Maximum value normalized to 1")
    
    # Test Case 3: Middle value (5) normalizes to 0.5
    assert abs(test_df['rating_normalized'].iloc[1] - 0.5) < 0.001, \
        "Test 3 failed: Middle value not normalized to 0.5"
    print("[PASS] Test 3: Middle value normalized to 0.5")
    
    print("All rating normalization tests passed!\n")

# ============================================================================
# STEP 5: Generate Summary Report
# ============================================================================

def generate_summary_report(df_before, df_after):
    """
    Generate a comprehensive before vs after summary report.
    
    Args:
        df_before (DataFrame): Original dataset
        df_after (DataFrame): Processed dataset
        
    Returns:
        dict: Summary statistics
    """
    report = {
        'before': {},
        'after': {}
    }
    
    # Record counts
    report['before']['total_records'] = len(df_before)
    report['after']['total_records'] = len(df_after)
    
    # Missing values
    report['before']['missing_ratings'] = df_before['rating'].isna().sum()
    report['after']['missing_ratings'] = df_after['rating'].isna().sum()
    report['before']['missing_text'] = df_before['review_text'].isna().sum()
    report['after']['missing_text'] = df_after['review_text_standardized'].isna().sum()
    
    # Text length statistics
    df_before['text_length'] = df_before['review_text'].astype(str).str.len()
    df_after['text_length'] = df_after['review_text_standardized'].astype(str).str.len()
    
    report['before']['text_length_mean'] = df_before['text_length'].mean()
    report['before']['text_length_std'] = df_before['text_length'].std()
    report['before']['text_length_min'] = df_before['text_length'].min()
    report['before']['text_length_max'] = df_before['text_length'].max()
    
    report['after']['text_length_mean'] = df_after['text_length'].mean()
    report['after']['text_length_std'] = df_after['text_length'].std()
    report['after']['text_length_min'] = df_after['text_length'].min()
    report['after']['text_length_max'] = df_after['text_length'].max()
    
    # Rating distribution
    report['before']['rating_mean'] = df_before['rating'].mean()
    report['before']['rating_std'] = df_before['rating'].std()
    report['before']['rating_min'] = df_before['rating'].min()
    report['before']['rating_max'] = df_before['rating'].max()
    
    report['after']['rating_mean'] = df_after['rating'].mean()
    report['after']['rating_std'] = df_after['rating'].std()
    report['after']['rating_min'] = df_after['rating'].min()
    report['after']['rating_max'] = df_after['rating'].max()
    
    report['after']['rating_normalized_mean'] = df_after['rating_normalized'].mean()
    report['after']['rating_normalized_std'] = df_after['rating_normalized'].std()
    report['after']['rating_normalized_min'] = df_after['rating_normalized'].min()
    report['after']['rating_normalized_max'] = df_after['rating_normalized'].max()
    
    return report

def print_summary_report(report):
    """
    Print formatted summary report.
    """
    print("\n" + "="*80)
    print("BEFORE vs AFTER SUMMARY REPORT")
    print("="*80)
    
    print("\n[RECORD COUNTS]")
    print(f"  Before: {report['before']['total_records']} records")
    print(f"  After:  {report['after']['total_records']} records")
    
    print("\n[MISSING VALUES]")
    print(f"  Ratings - Before: {report['before']['missing_ratings']}, After: {report['after']['missing_ratings']}")
    print(f"  Text    - Before: {report['before']['missing_text']}, After: {report['after']['missing_text']}")
    
    print("\n[TEXT LENGTH STATISTICS]")
    print(f"  Before - Mean: {report['before']['text_length_mean']:.2f}, "
          f"Std: {report['before']['text_length_std']:.2f}, "
          f"Min: {report['before']['text_length_min']}, "
          f"Max: {report['before']['text_length_max']}")
    print(f"  After  - Mean: {report['after']['text_length_mean']:.2f}, "
          f"Std: {report['after']['text_length_std']:.2f}, "
          f"Min: {report['after']['text_length_min']}, "
          f"Max: {report['after']['text_length_max']}")
    
    print("\n[RATING DISTRIBUTION - Original 0-10 scale]")
    print(f"  Before - Mean: {report['before']['rating_mean']:.2f}, "
          f"Std: {report['before']['rating_std']:.2f}, "
          f"Min: {report['before']['rating_min']:.2f}, "
          f"Max: {report['before']['rating_max']:.2f}")
    print(f"  After  - Mean: {report['after']['rating_mean']:.2f}, "
          f"Std: {report['after']['rating_std']:.2f}, "
          f"Min: {report['after']['rating_min']:.2f}, "
          f"Max: {report['after']['rating_max']:.2f}")
    
    print("\n[RATING DISTRIBUTION - Normalized 0-1 scale]")
    print(f"  After  - Mean: {report['after']['rating_normalized_mean']:.4f}, "
          f"Std: {report['after']['rating_normalized_std']:.4f}, "
          f"Min: {report['after']['rating_normalized_min']:.4f}, "
          f"Max: {report['after']['rating_normalized_max']:.4f}")
    
    print("\n" + "="*80 + "\n")

# ============================================================================
# MAIN PREPROCESSING PIPELINE
# ============================================================================

def preprocess_movie_reviews(input_file='movie_reviews-1.csv', output_file='movie_reviews_cleaned.csv'):
    """
    Main preprocessing pipeline for movie reviews data.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        
    Returns:
        DataFrame: Cleaned and preprocessed dataset
    """
    print("="*80)
    print("MOVIE REVIEWS DATA CLEANING AND PREPROCESSING")
    print("="*80)
    
    # Load dataset
    print(f"\n[LOAD] Loading dataset from: {input_file}")
    df = pd.read_csv(input_file)
    df_before = df.copy()
    print(f"   Loaded {len(df)} records")
    
    # Step 1: Standardize review text
    print("\n[STEP 1] Standardizing review text...")
    df['review_text_standardized'] = df['review_text'].apply(standardize_text)
    print("   [OK] Text standardized (lowercase, HTML tags removed)")
    
    # Step 2: Tokenize and encode using TF-IDF
    print("\n[STEP 2] Tokenizing and encoding reviews using TF-IDF...")
    df, vectorizer = tokenize_and_encode_tfidf(df, max_features=50)
    print(f"   [OK] Reviews encoded with {len([c for c in df.columns if c.startswith('tfidf_')])} TF-IDF features")
    
    # Step 3: Handle missing ratings
    print("\n[STEP 3] Handling missing ratings...")
    df, median_rating = handle_missing_ratings(df)
    print(f"   [OK] Missing ratings filled with median: {median_rating:.2f}")
    
    # Step 4: Normalize ratings
    print("\n[STEP 4] Normalizing ratings from 0-10 to 0-1 scale...")
    df = normalize_ratings(df)
    print("   [OK] Ratings normalized to 0-1 scale")
    
    # Step 5: Generate summary report
    print("\n[STEP 5] Generating summary report...")
    report = generate_summary_report(df_before, df)
    print_summary_report(report)
    
    # Save cleaned dataset
    print(f"\n[SAVE] Saving cleaned dataset to: {output_file}")
    df.to_csv(output_file, index=False)
    print("   [OK] Dataset saved successfully")
    
    return df, report

# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """
    Run all test cases.
    """
    print("\n" + "="*80)
    print("RUNNING ALL TEST CASES")
    print("="*80)
    
    test_standardize_text()
    test_tokenize_and_encode()
    test_handle_missing_ratings()
    test_normalize_ratings()
    
    print("="*80)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("="*80)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run all tests first
    run_all_tests()
    
    # Run preprocessing pipeline
    cleaned_data, summary_report = preprocess_movie_reviews()
    
    print("\n[SUCCESS] Preprocessing complete! Dataset is ready for sentiment classification.")
    print(f"\n[OUTPUT] Output file: movie_reviews_cleaned.csv")
    print(f"[STATS] Total records: {len(cleaned_data)}")
    print(f"[STATS] Total features: {len(cleaned_data.columns)}")

