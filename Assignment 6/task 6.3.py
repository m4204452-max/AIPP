from __future__ import annotations


def classify_age(age: int) -> str:
    """
    Classify a person's age into categories using match/case conditionals.
    """
    match age:
        case value if value < 0:
            raise ValueError("age must be non-negative")
        case value if value <= 2:
            return "Infant"
        case value if value <= 5:
            return "Toddler"
        case value if value <= 12:
            return "Child"
        case value if value <= 17:
            return "Teenager"
        case value if value <= 59:
            return "Adult"
        case _:
            return "Senior"


if __name__ == "__main__":
    sample_ages = [1, 4, 8, 15, 30, 65]
    for age_value in sample_ages:
        print(f"Age {age_value}: {classify_age(age_value)}")

