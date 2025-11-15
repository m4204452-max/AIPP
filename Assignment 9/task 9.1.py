from typing import Iterable, Tuple


def sum_even_and_odd(numbers: Iterable[int]) -> Tuple[int, int]:
    """Return the sums of even and odd numbers in the given list.

    Args:
        numbers: A list (or iterable) of integers to evaluate.

    Returns:
        A tuple of two integers:
        - even_sum: Sum of all even numbers.
        - odd_sum: Sum of all odd numbers.

    Raises:
        TypeError: If any element in numbers is not an int.

    Examples:
        >>> sum_even_and_odd([1, 2, 3, 4])
        (6, 4)
        >>> sum_even_and_odd([])
        (0, 0)
    """
    even_sum: int = 0
    odd_sum: int = 0

    for value in numbers:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("All elements must be integers (bool is not allowed).")
        if value % 2 == 0:
            even_sum += value
        else:
            odd_sum += value

    return even_sum, odd_sum


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6]
    even_total, odd_total = sum_even_and_odd(data)
    print(f"Input: {data}")
    print(f"Even sum: {even_total}, Odd sum: {odd_total}")


