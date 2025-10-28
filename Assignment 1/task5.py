"""
Find the largest number in a list.

This file provides two implementations:
 - manual_max(lst): an explicit iterative implementation that validates input
 - builtin_max(lst): a thin wrapper around Python's built-in max with validation

Both functions raise a ValueError for an empty list and TypeError for non-numeric
elements. Example usage is included in the `main()` function.
"""

from typing import List, Union

Number = Union[int, float]


def manual_max(lst: List[Number]) -> Number:
	"""Return the largest number in lst using an explicit iteration.

	Raises:
		ValueError: if lst is empty
		TypeError: if any element in lst is not an int or float

	Time complexity: O(n) where n = len(lst)
	Space complexity: O(1) additional space
	"""
	if not isinstance(lst, list):
		raise TypeError("Input must be a list")

	if len(lst) == 0:
		raise ValueError("Cannot determine max of an empty list")

	# Initialize with first element after validating its type
	first = lst[0]
	if not isinstance(first, (int, float)):
		raise TypeError("List must contain only numeric values (int or float)")
	current_max = first

	# Iterate through remaining elements and update current_max
	for x in lst[1:]:
		if not isinstance(x, (int, float)):
			raise TypeError("List must contain only numeric values (int or float)")
		if x > current_max:
			current_max = x

	return current_max


def builtin_max(lst: List[Number]) -> Number:
	"""Return the largest number in lst using Python's built-in max.

	This function adds validation and clearer error messages on failure.

	Time complexity: O(n)
	Space complexity: O(1) additional space
	"""
	if not isinstance(lst, list):
		raise TypeError("Input must be a list")
	if len(lst) == 0:
		raise ValueError("Cannot determine max of an empty list")

	# Using built-in max for clarity and C-level speed. We still try to give
	# a helpful error if non-comparable elements are present.
	try:
		result = max(lst)
	except TypeError:
		# Provide a clearer explanation than default if mixed/uncomparable types
		raise TypeError("List contains non-comparable or non-numeric items")

	# Optionally validate numeric type of result (max could return non-numeric
	# if list contains such elements but they were comparable). Enforce numeric.
	if not isinstance(result, (int, float)):
		raise TypeError("List must contain numeric values (int or float)")

	return result


def main():
	examples = [
		[3, 1, 7, 4],
		[-5, -2, -10],
		[1.5, 2.7, 0.3],
		# Uncomment to see error handling examples:
		# [],
		# [3, 'a', 5],
	]

	for lst in examples:
		print("list:", lst)
		try:
			print("  manual_max ->", manual_max(lst))
		except Exception as e:
			print("  manual_max raised:", type(e).__name__, "-", e)

		try:
			print("  builtin_max->", builtin_max(lst))
		except Exception as e:
			print("  builtin_max raised:", type(e).__name__, "-", e)


if __name__ == "__main__":
	main()

