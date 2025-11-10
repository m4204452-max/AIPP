from __future__ import annotations
from typing import List


def first_ten_multiples_while(number: int) -> List[int]:
    """
    Returns the first ten positive multiples of `number` using a while loop.
    """
    multiples: List[int] = []
    multiplier = 1
    while multiplier <= 10:
        multiples.append(number * multiplier)
        multiplier += 1
    return multiples


if __name__ == "__main__":
    value = 5
    result = first_ten_multiples_while(value)
    print(f"First 10 multiples of {value} (while): {result}")

