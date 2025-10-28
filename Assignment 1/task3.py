def reverse_string(input_string):
    # Using string slicing with step -1 to reverse the string
    return input_string[::-1]

def main():
    # Get input string from user
    user_string = input("Enter a string to reverse: ")
    
    # Get the reversed string
    reversed_string = reverse_string(user_string)
    
    # Print the result
    print(f"Original string: {user_string}")
    print(f"Reversed string: {reversed_string}")

if __name__ == "__main__":
    main()
