def is_leap_year(year):
    """
    Check whether a given year is a leap year.
    
    A year is a leap year if:
    - It is divisible by 4, AND
    - It is NOT divisible by 100, OR
    - It IS divisible by 400
    
    Args:
        year (int): The year to check
        
    Returns:
        bool: True if the year is a leap year, False otherwise
    """
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


# Alternative concise version:
# def is_leap_year(year):
#     return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_years = [2000, 1900, 2024, 2023, 2004, 2100]
    
    print("Leap Year Checker")
    print("=" * 30)
    
    for year in test_years:
        result = is_leap_year(year)
        status = "Leap Year" if result else "Not a Leap Year"
        print(f"{year}: {status}")
    
    # Interactive version
    print("\n" + "=" * 30)
    try:
        year = int(input("Enter a year to check: "))
        if is_leap_year(year):
            print(f"{year} is a leap year.")
        else:
            print(f"{year} is not a leap year.")
    except ValueError:
        print("Please enter a valid integer year.")