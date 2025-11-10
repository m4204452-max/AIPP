# task 5.3.py - Recursive Fibonacci Calculator

def fibonacci_recursive(n: int) -> int:
    """
    Return the nth Fibonacci number using recursion.
    """
    # Guard clause: Fibonacci is defined for non-negative integers only
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    # Base case 1: F(0) = 0
    if n == 0:
        return 0

    # Base case 2: F(1) = 1
    if n == 1:
        return 1

    # Recursive case: F(n) = F(n-1) + F(n-2)
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


if __name__ == "__main__":
    # Example usage
    try:
        n = int(input("Enter n (non-negative integer): "))
        print(f"F({n}) = {fibonacci_recursive(n)}")
    except ValueError as exc:
        print(f"Error: {exc}")