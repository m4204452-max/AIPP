# Manual comments are provided inline below each statement/block.
# AI-style comments are also included, prefixed with "AI:" to distinguish them.

from dataclasses import dataclass
from typing import Optional


@dataclass
class SRUStudent:
    # Define core attributes for a student.
    # AI: Data attributes represent the student's identity and accommodation flag.
    name: str
    roll_no: int
    hostel_status: bool

    # Total fee is derived after calling fee_update; start as None until computed.
    # AI: This stores the computed payable amount after applying the update rules.
    total_fee: Optional[float] = None

    def fee_update(self, base_fee: float, hostel_fee: float = 0.0) -> None:
        # Compute payable fee based on hostel status.
        # AI: Adds hostel component only if hostel_status is True.
        if base_fee < 0 or hostel_fee < 0:
            # Guard against invalid negative inputs.
            # AI: Validate inputs to prevent nonsensical negative fees.
            raise ValueError("base_fee and hostel_fee must be non-negative.")

        if self.hostel_status:
            # If in hostel, add hostel_fee to base.
            # AI: Conditional branch for residents.
            self.total_fee = float(base_fee + hostel_fee)
        else:
            # If not in hostel, base_fee is the total.
            # AI: Non-residents pay academic component only.
            self.total_fee = float(base_fee)

    def display_details(self) -> str:
        # Build a human-readable summary of the student's details.
        # AI: Compose a formatted string, including fee if available.
        fee_str = "Not computed" if self.total_fee is None else f"{self.total_fee:.2f}"
        return (
            f"Name: {self.name}, "
            f"Roll No: {self.roll_no}, "
            f"Hostel: {'Yes' if self.hostel_status else 'No'}, "
            f"Total Fee: {fee_str}"
        )


if __name__ == "__main__":
    # Example usage demonstrating both methods.
    # AI: Create instances and show fee computation and display.
    student_day = SRUStudent(name="Aisha Khan", roll_no=101, hostel_status=False)
    student_hostel = SRUStudent(name="Ravi Kumar", roll_no=102, hostel_status=True)

    # Update fees: hostel student gets hostel component added.
    # AI: Call fee_update; totals differ based on hostel_status.
    student_day.fee_update(base_fee=50000.0, hostel_fee=20000.0)
    student_hostel.fee_update(base_fee=50000.0, hostel_fee=20000.0)

    # Print details for verification.
    # AI: Show the string returned by display_details.
    print(student_day.display_details())
    print(student_hostel.display_details())



