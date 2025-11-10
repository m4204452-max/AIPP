
from itertools import accumulate

def sum_first_ten_accumulate() -> int:
    return list(accumulate(range(1, 11)))[-1]