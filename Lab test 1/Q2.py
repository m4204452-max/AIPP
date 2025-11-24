"""Refactored helper with AI-generated documentation."""


def calculate_discounted_total(prices, tax_rate, discount_threshold=100, discount_rate=0.1):
    """Return the final payable amount after tax and conditional discount.

    Args:
        prices (Iterable[float]): Individual item prices.
        tax_rate (float): Tax percentage expressed as decimal (e.g., 0.08 for 8%).
        discount_threshold (float, optional): Subtotal required to unlock the discount.
        discount_rate (float, optional): Discount percentage (decimal) applied when threshold met.

    Raises:
        ValueError: If inputs are empty or contain negative numbers.

    Returns:
        float: Final amount rounded to two decimal places.
    """
    if not prices:
        raise ValueError("Provide at least one price")

    if any(price < 0 for price in prices):
        raise ValueError("Prices must be non-negative")

    subtotal = sum(prices)
    taxed_total = subtotal * (1 + tax_rate)

    # Apply discount only when taxed total passes threshold to reflect billing rules.
    if taxed_total >= discount_threshold:
        taxed_total *= (1 - discount_rate)

    return round(taxed_total, 2)


if __name__ == "__main__":
    sample = [25.0, 45.5, 60.0]
    print("Final total:", calculate_discounted_total(sample, tax_rate=0.07))
