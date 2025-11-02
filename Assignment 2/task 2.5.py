def even_odd_stats(nums):
    """
    Given an iterable of integers, return a dict:
      {'even_count': int, 'odd_count': int, 'even_sum': int, 'odd_sum': int}
    """
    even_count = odd_count = even_sum = odd_sum = 0
    for n in nums:
        if n % 2 == 0:
            even_count += 1
            even_sum += n
        else:
            odd_count += 1
            odd_sum += n
    return {
        'even_count': even_count,
        'odd_count': odd_count,
        'even_sum': even_sum,
        'odd_sum': odd_sum,
    }

# Example
print(even_odd_stats([1,2,3,4,5]))  # -> {'even_count':2,'odd_count':3,'even_sum':6,'odd_sum':9}