def is_prime(number):
    """
    Check if a number is prime.
    Returns True if the number is prime, False otherwise.
    """
    # Check if number is less than 2 (not prime)
    if number < 2:
        return False
    
    # Check if number is 2 (prime)
    if number == 2:
        return True
    
    # Check if number is even (not prime, except 2)
    if number % 2 == 0:
        return False
    
    # Check for divisibility from 3 to square root of number, step by 2
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            return False
    
    return True

def main():
    try:
        # Get input from user
        num = int(input("Enter a number to check if it's prime: "))
        
        # Check if the number is prime
        if is_prime(num):
            print(f"{num} is a prime number")
        else:
            print(f"{num} is not a prime number")
            
    except ValueError:
        print("Please enter a valid integer number")

# Example usage
if __name__ == "__main__":
    main()