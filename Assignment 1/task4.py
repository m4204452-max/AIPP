# Recursive version of factorial
def factorial_recursive(n):
    """
    Calculate factorial using recursion
    n! = n * (n-1)!
    Base case: 0! = 1
    """
    # Base cases
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    
    # Recursive case: n! = n * (n-1)!
    return n * factorial_recursive(n - 1)

# Iterative version of factorial
def factorial_iterative(n):
    """
    Calculate factorial using iteration
    n! = n * (n-1) * (n-2) * ... * 2 * 1
    """
    # Check for negative numbers
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Initialize result to 1 (empty product)
    result = 1
    
    # Multiply numbers from 1 to n
    for i in range(1, n + 1):
        result *= i
    
    return result

def main():
    try:
        # Get input from user
        num = int(input("Enter a number to calculate its factorial: "))
        
        # Calculate factorial using both methods
        print(f"\nCalculating factorial of {num}:")
        print(f"Using recursive method: {factorial_recursive(num)}")
        print(f"Using iterative method: {factorial_iterative(num)}")
        
    except ValueError as e:
        # Handle both invalid input and negative numbers
        if "negative numbers" in str(e):
            print(e)
        else:
            print("Please enter a valid integer number")

if __name__ == "__main__":
    main()
