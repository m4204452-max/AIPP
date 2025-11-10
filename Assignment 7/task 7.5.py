numbers = [1, 2, 3]
index = 5

# Option 1: Check length before indexing
if 0 <= index < len(numbers):
    print(numbers[index])
else:
    print("Index out of range")

# Option 2: Safe access helper (returns default if out of range)
def get_or_default(seq, idx, default=None):
    return seq[idx] if 0 <= idx < len(seq) else default

print(get_or_default(numbers, index, default="N/A"))

