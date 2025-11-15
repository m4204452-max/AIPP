"""
Calculator Module

This module provides basic arithmetic operations for performing calculations.

AI-Generated Module Docstring:
    This module implements a simple calculator with four fundamental arithmetic
    operations: addition, subtraction, multiplication, and division. Each function
    handles numeric inputs and returns the computed result, with division
    including protection against division by zero errors.
"""


def add(a: float, b: float) -> float:
    """
    Add two numbers.

    Parameters
    ----------
    a : float
        First number to be added.
    b : float
        Second number to be added.

    Returns
    -------
    float
        Sum of a and b.

    Examples
    --------
    >>> add(5, 3)
    8.0
    >>> add(-2, 7)
    5.0
    >>> add(0, 0)
    0.0

    AI-Generated Docstring:
        Adds two numeric values together.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.

        Raises:
            TypeError: If either argument is not a number.
    """
    return float(a + b)


def subtract(a: float, b: float) -> float:
    """
    Subtract second number from first number.

    Parameters
    ----------
    a : float
        The minuend (number to subtract from).
    b : float
        The subtrahend (number to subtract).

    Returns
    -------
    float
        Difference of a and b (a - b).

    Examples
    --------
    >>> subtract(10, 4)
    6.0
    >>> subtract(5, 8)
    -3.0
    >>> subtract(0, 0)
    0.0

    AI-Generated Docstring:
        Subtracts the second number from the first number.

        Args:
            a (float): The minuend.
            b (float): The subtrahend.

        Returns:
            float: The result of a - b.

        Raises:
            TypeError: If either argument is not a number.
    """
    return float(a - b)


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Parameters
    ----------
    a : float
        First multiplicand.
    b : float
        Second multiplicand.

    Returns
    -------
    float
        Product of a and b.

    Examples
    --------
    >>> multiply(3, 4)
    12.0
    >>> multiply(-2, 5)
    -10.0
    >>> multiply(0, 100)
    0.0

    AI-Generated Docstring:
        Multiplies two numbers together.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.

        Raises:
            TypeError: If either argument is not a number.
    """
    return float(a * b)


def divide(a: float, b: float) -> float:
    """
    Divide first number by second number.

    Parameters
    ----------
    a : float
        The dividend (number to be divided).
    b : float
        The divisor (number to divide by). Must not be zero.

    Returns
    -------
    float
        Quotient of a divided by b (a / b).

    Raises
    ------
    ZeroDivisionError
        If b is zero.

    Examples
    --------
    >>> divide(10, 2)
    5.0
    >>> divide(7, 2)
    3.5
    >>> divide(-15, 3)
    -5.0

    AI-Generated Docstring:
        Divides the first number by the second number.

        Args:
            a (float): The dividend.
            b (float): The divisor (must not be zero).

        Returns:
            float: The result of a / b.

        Raises:
            ZeroDivisionError: If b is zero.
            TypeError: If either argument is not a number.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return float(a / b)


if __name__ == "__main__":
    # Demonstration of all calculator functions
    print("Calculator Module Demo")
    print("=" * 40)
    
    # Test addition
    result_add = add(15, 7)
    print(f"add(15, 7) = {result_add}")
    
    # Test subtraction
    result_sub = subtract(20, 8)
    print(f"subtract(20, 8) = {result_sub}")
    
    # Test multiplication
    result_mul = multiply(6, 9)
    print(f"multiply(6, 9) = {result_mul}")
    
    # Test division
    result_div = divide(45, 5)
    print(f"divide(45, 5) = {result_div}")
    
    # Test division by zero error handling
    try:
        divide(10, 0)
    except ZeroDivisionError as e:
        print(f"Error caught: {e}")


