def format_name_last_first(full_name):
    """
    Format a full name from "First Last" to "Last, First" format.
    
    This function takes a full name string and rearranges it to display
    the last name first, followed by a comma and space, then the first name.
    
    Args:
        full_name (str): The full name in "First Last" format
        
    Returns:
        str: The name formatted as "Last, First"
        
    Examples:
        >>> format_name_last_first("John Doe")
        'Doe, John'
        >>> format_name_last_first("Jane Smith")
        'Smith, Jane'
        >>> format_name_last_first("Mary Johnson")
        'Johnson, Mary'
    """
    # Split the name into parts
    name_parts = full_name.strip().split()
    
    # Handle cases with at least first and last name
    if len(name_parts) >= 2:
        # First name is everything except the last word
        first_name = " ".join(name_parts[:-1])
        # Last name is the last word
        last_name = name_parts[-1]
        return f"{last_name}, {first_name}"
    else:
        # If only one word or empty, return as is (or handle error)
        return full_name


# Example usage and testing
if __name__ == "__main__":
    print("Name Formatter: Last, First")
    print("=" * 50)
    print("Enter 3 full names to format (First Last format):\n")
    
    # Get 3 names from the user
    names = []
    for i in range(3):
        try:
            name = input(f"Enter name {i + 1}: ").strip()
            if name:
                names.append(name)
            else:
                print("Empty name entered, skipping...")
        except Exception as e:
            print(f"Error reading input: {e}")
    
    # Display formatted names
    if names:
        print("\n" + "=" * 50)
        print("Formatted Names:")
        print("-" * 50)
        print(f"{'Original Name':<30} {'Formatted Name':<30}")
        print("-" * 50)
        
        for name in names:
            formatted = format_name_last_first(name)
            print(f"{name:<30} {formatted:<30}")
    else:
        print("No names were entered.")
