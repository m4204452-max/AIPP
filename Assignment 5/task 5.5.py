"""
task 5.5.py — Gender-neutral team roster management

This example shows how to:
1. Store people without gendered fields.
2. Refer to them with inclusive pronouns (“they/them”).
3. Build messages that avoid gendered language.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TeamMember:
    """Represents a person on the team without gendered attributes."""
    name: str
    role: str
    years_experience: int

    def introduction(self) -> str:
        """Return a gender-neutral introduction."""
        pronoun = "they"
        possessive = "their"
        return (
            f"{self.name} is our {self.role}. "
            f"{pronoun.capitalize()} bring {possessive} "
            f"{self.years_experience} years of experience."
        )


class TeamRoster:
    """Manages a team roster using gender-neutral language."""

    def __init__(self) -> None:
        self._members: List[TeamMember] = []

    def add_member(self, member: TeamMember) -> None:
        """Add a new team member."""
        self._members.append(member)

    def summary(self) -> str:
        """Generate a gender-neutral summary of the team."""
        if not self._members:
            return "Our team is growing—stay tuned for new members."

        introductions = [member.introduction() for member in self._members]
        return "\n".join(introductions)

    def inclusive_greeting(self) -> str:
        """Return an inclusive greeting for the whole team."""
        names = ", ".join(member.name for member in self._members) or "everyone"
        return (
            f"Hello {names}! We appreciate each person’s unique contributions. "
            "Let’s continue supporting one another."
        )


if __name__ == "__main__":
    # Example usage
    roster = TeamRoster()
    roster.add_member(TeamMember("Alex Taylor", "lead engineer", 7))
    roster.add_member(TeamMember("Jordan Lee", "product strategist", 5))
    roster.add_member(TeamMember("Sam Rivera", "user researcher", 3))

    print("=== Team Summary ===")
    print(roster.summary())
    print("\n=== Inclusive Greeting ===")
    print(roster.inclusive_greeting())