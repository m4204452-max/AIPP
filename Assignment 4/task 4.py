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
        >>> count_vowels("Hello World")
        3
        >>> count_vowels("Python Programming")
        4
        >>> count_vowels("AEIOU")
        5
        >>> count_vowels("xyz")
        0
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


# Alternative concise version using list comprehension:
# def count_vowels(text):
#     return sum(1 for char in text.lower() if char in "aeiou")


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_strings = [
        "Hello World",
        "Python Programming",
        "AEIOU",
        "aeiou",
        "xyz",
        "The quick brown fox jumps over the lazy dog",
        "Case Insensitive TEST"
    ]
    
    print("Vowel Counter")
    print("=" * 50)
    print(f"{'String':<40} {'Vowel Count':<15}")
    print("-" * 50)
    
    for test_string in test_strings:
        vowel_count = count_vowels(test_string)
        print(f"{test_string:<40} {vowel_count:<15}")
    
    # Interactive version
    print("\n" + "=" * 50)
    try:
        user_input = input("Enter a string to count vowels: ")
        vowel_count = count_vowels(user_input)
        print(f"Number of vowels in '{user_input}': {vowel_count}")
    except Exception as e:
        print(f"Error: {e}")


