def cm_to_inches(cm):
    """
    Convert centimeters to inches.
    
    Conversion factor: 1 inch = 2.54 centimeters
    
    Args:
        cm (float): Length in centimeters
        
    Returns:
        float: Length in inches
        
    Examples:
        >>> cm_to_inches(2.54)
        1.0
        >>> cm_to_inches(10)
        3.937007874015748
        >>> cm_to_inches(0)
        0.0
    """
    return cm / 2.54


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_values = [2.54, 10, 25.4, 0, 100, 1]
    
    print("Centimeters to Inches Converter")
    print("=" * 40)
    print(f"{'Centimeters':<15} {'Inches':<15}")
    print("-" * 40)
    
    for cm in test_values:
        inches = cm_to_inches(cm)
        print(f"{cm:<15.2f} {inches:<15.4f}")
    
    # Interactive version
    print("\n" + "=" * 40)
    try:
        cm_value = float(input("Enter length in centimeters: "))
        inches_value = cm_to_inches(cm_value)
        print(f"{cm_value} cm = {inches_value:.4f} inches")
    except ValueError:
        print("Please enter a valid number.")