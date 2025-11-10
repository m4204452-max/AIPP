from __future__ import annotations
from typing import Dict, Iterable, Tuple


class Student:
    """
    Represents a student with basic identity fields and simple academic records.

    Attributes:
        first_name: Given name of the student.
        last_name: Family name of the student.
        student_id: Unique identifier for the student.
        course_to_grade_points: Mapping of course code/name to earned grade points (0.0 - 4.0).
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        student_id: str,
        courses: Iterable[Tuple[str, float]] | None = None,
    ) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.student_id: str = student_id
        self.course_to_grade_points: Dict[str, float] = {}

        if courses:
            for course, grade_points in courses:
                self.add_course(course, grade_points)

    # ---------- Convenience methods ----------
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def add_course(self, course: str, grade_points: float) -> None:
        """
        Adds or updates a course grade.

        grade_points should be in the inclusive range [0.0, 4.0].
        """
        if not (0.0 <= grade_points <= 4.0):
            raise ValueError("grade_points must be between 0.0 and 4.0 inclusive")
        self.course_to_grade_points[course] = grade_points

    def calculate_gpa(self) -> float:
        """
        Calculates a simple GPA as the arithmetic mean of grade points.
        Returns 0.0 if the student has no courses.
        """
        if not self.course_to_grade_points:
            return 0.0
        total_points = sum(self.course_to_grade_points.values())
        num_courses = len(self.course_to_grade_points)
        return round(total_points / num_courses, 2)

    # ---------- Representations ----------
    def __repr__(self) -> str:
        return (
            f"Student(first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, "
            f"student_id={self.student_id!r}, "
            f"courses={list(self.course_to_grade_points.items())!r})"
        )

    def __str__(self) -> str:
        gpa = self.calculate_gpa()
        return (
            f"{self.full_name()} (ID: {self.student_id}) — "
            f"{len(self.course_to_grade_points)} courses, GPA: {gpa:.2f}"
        )


if __name__ == "__main__":
    # Demo: create a student and print results
    student = Student(
        first_name="Ada",
        last_name="Lovelace",
        student_id="S12345",
        courses=[("Math", 4.0), ("Algorithms", 3.7)],
    )

    print("Initial state:")
    print(student)  # Uses __str__

    # Update with a new course and show recalculated GPA
    student.add_course("Data Science", 3.3)

    print("\nAfter adding Data Science:")
    print("Full name:", student.full_name())
    print("Courses:", student.course_to_grade_points)
    print("GPA:", student.calculate_gpa())

    # Developer-oriented representation
    print("\nDebug repr:")
    print(repr(student))

