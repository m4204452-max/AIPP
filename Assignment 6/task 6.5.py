from __future__ import annotations


class BankAccount:
    """
    Simple bank account model supporting deposits, withdrawals, and balance inquiry.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        # Account holder's name
        self.owner: str = owner
        # Current account balance; ensure it never falls below zero
        self._balance: float = 0.0
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._balance = float(initial_balance)

    def deposit(self, amount: float) -> None:
        """
        Add funds to the account.

        Raises:
            ValueError: If the deposit amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Remove funds from the account if sufficient balance is available.

        Raises:
            ValueError: If the withdrawal amount is not positive or exceeds balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount

    def get_balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def __str__(self) -> str:
        """Human-readable summary of the account state."""
        return f"BankAccount(owner={self.owner}, balance={self._balance:.2f})"


if __name__ == "__main__":
    # Demonstration of class usage
    account = BankAccount(owner="Alex Doe", initial_balance=100.0)
    print("Initial:", account)  # Uses __str__ for readable output

    account.deposit(50.0)
    print("After deposit:", account.get_balance())

    account.withdraw(30.0)
    print("After withdrawal:", account)  # Still uses __str__

