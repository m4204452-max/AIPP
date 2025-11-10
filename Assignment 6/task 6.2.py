from __future__ import annotations
from typing import List


def first_ten_multiples(number: int) -> List[int]:
    """
    Returns the first ten positive multiples of `number`.

    Examples:
        >>> first_ten_multiples(3)
        [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    """
    multiples: List[int] = []
    for multiplier in range(1, 11):
        multiples.append(number * multiplier)
    return multiples


if __name__ == "__main__":
    value = 7
    result = first_ten_multiples(value)
    print(f"First 10 multiples of {value}: {result}")

