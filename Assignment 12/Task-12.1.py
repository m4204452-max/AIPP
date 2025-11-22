def linear_search(arr, value):
    """
    Perform a linear search to find the index of 'value' in 'arr'.
    Returns the index if found, else returns -1.
    """
    for index, item in enumerate(arr):
        if item == value:
            return index
    return -1
    # Example usage and output
if __name__ == "__main__":
    arr = [23, 45, 12, 67, 34]
    value = 67
    result = linear_search(arr, value)
    print(f"Searching for {value} in {arr}")
    if result != -1:
        print(f"Element found at index {result}")
    else:
        print("Element not found.")

