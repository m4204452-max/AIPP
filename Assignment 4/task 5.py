def count_lines(filename):
    """
    Read a .txt file and return the number of lines.
    
    This function opens a text file, reads its contents, and counts the
    total number of lines in the file (including empty lines).
    
    Args:
        filename (str): The path to the .txt file to read
        
    Returns:
        int: The number of lines in the file
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
        
    Examples:
        >>> count_lines("example.txt")
        10
        >>> count_lines("data.txt")
        25
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_count = 0
            for line in file:
                line_count += 1
            return line_count
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except IOError as e:
        raise IOError(f"Error reading file '{filename}': {e}")


# Alternative concise version:
# def count_lines(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         return sum(1 for line in file)


# Example usage and testing
if __name__ == "__main__":
    print("File Line Counter")
    print("=" * 50)
    
    # Example: Get filename from user
    try:
        filename = input("Enter the path to a .txt file: ").strip()
        
        if not filename:
            print("No filename provided.")
        else:
            # Ensure it's a .txt file (optional check)
            if not filename.endswith('.txt'):
                print(f"Warning: '{filename}' does not have a .txt extension.")
                response = input("Do you want to continue? (y/n): ").strip().lower()
                if response != 'y':
                    print("Operation cancelled.")
                    exit()
            
            line_count = count_lines(filename)
            print(f"\nFile: {filename}")
            print(f"Number of lines: {line_count}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

