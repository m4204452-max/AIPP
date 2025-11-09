def count_vowels(text):
    """
    Count the number of vowels in a string (case insensitive).
    
    This function counts all occurrences of vowels (a, e, i, o, u) in a given
    string. The counting is case insensitive, meaning both uppercase and
    lowercase vowels are counted.
    
    Args:
        text (str): The string to count vowels in
        
    Returns:
        int: The number of vowels in the string
        
    Examples:
        >>> count_vowels("Hello")
        2
        >>> count_vowels("Python")
        1
        >>> count_vowels("AEIOU")
        5
        >>> count_vowels("Xyz")
        0
        >>> count_vowels("Hello World")
        3
    """
    # Convert to lowercase for case-insensitive comparison
    text_lower = text.lower()
    
    # Define vowels
    vowels = "aeiou"
    
    # Count vowels
    count = 0
    for char in text_lower:
        if char in vowels:
            count += 1
    
    return count


# Example usage and testing
if __name__ == "__main__":
    # Test cases with the provided examples
    test_strings = [
        "Hello",
        "Python",
        "AEIOU",
        "Xyz",
        "Hello World"
    ]
    
    print("Vowel Counter")
    print("=" * 50)
    print(f"{'String':<20} {'Vowel Count':<15}")
    print("-" * 50)
    
    for test_string in test_strings:
        vowel_count = count_vowels(test_string)
        print(f"{test_string:<20} {vowel_count:<15}")

