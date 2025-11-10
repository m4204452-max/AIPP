# task 5.4.py - Fair Job Applicant Scoring System

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Applicant:
    name: str
    gender: str  # Stored for reporting only; not used in scoring
    years_experience: int
    education_level: str  # e.g., "High School", "Bachelor", "Master", "PhD"
    technical_assessment: float  # score out of 100
    soft_skills: float  # score out of 100
    certifications: List[str]
    leadership_experience: bool
    relevant_projects: int


class ApplicantScoringSystem:
    def __init__(self):
        # Scoring weights (gender-neutral, based purely on qualifications)
        self.weights = {
            "experience": 0.25,
            "education": 0.20,
            "technical_assessment": 0.25,
            "soft_skills": 0.10,
            "certifications": 0.10,
            "leadership": 0.05,
            "projects": 0.05,
        }
        # Map education level to points
        self.education_points = {
            "High School": 0.2,
            "Associate": 0.4,
            "Bachelor": 0.6,
            "Master": 0.8,
            "PhD": 1.0,
        }

    def score_applicant(self, applicant: Applicant) -> Dict[str, float]:
        """Calculate a composite score for an applicant."""
        # Feature 1: Work experience (normalized by capping at 10 years)
        experience_score = min(applicant.years_experience, 10) / 10

        # Feature 2: Education level (mapped via dictionary)
        education_score = self.education_points.get(applicant.education_level, 0.0)

        # Feature 3: Technical assessment (normalize to 0-1)
        technical_score = applicant.technical_assessment / 100

        # Feature 4: Soft skills (normalize to 0-1)
        soft_skills_score = applicant.soft_skills / 100

        # Feature 5: Certifications (cap at 5 to avoid overweighting)
        certifications_score = min(len(applicant.certifications), 5) / 5

        # Feature 6: Leadership experience (Boolean, 1.0 or 0.0)
        leadership_score = 1.0 if applicant.leadership_experience else 0.0

        # Feature 7: Relevant projects (cap at 10)
        projects_score = min(applicant.relevant_projects, 10) / 10

        # Combine scores using weights
        composite_score = (
            experience_score * self.weights["experience"] +
            education_score * self.weights["education"] +
            technical_score * self.weights["technical_assessment"] +
            soft_skills_score * self.weights["soft_skills"] +
            certifications_score * self.weights["certifications"] +
            leadership_score * self.weights["leadership"] +
            projects_score * self.weights["projects"]
        ) * 100  # convert to percentage

        return {
            "composite_score": round(composite_score, 2),
            "experience_score": round(experience_score, 2),
            "education_score": round(education_score, 2),
            "technical_score": round(technical_score, 2),
            "soft_skills_score": round(soft_skills_score, 2),
            "certifications_score": round(certifications_score, 2),
            "leadership_score": round(leadership_score, 2),
            "projects_score": round(projects_score, 2),
        }

    def rank_applicants(self, applicants: List[Applicant]) -> List[Dict]:
        """Score and rank applicants from highest to lowest."""
        scored_applicants = []
        for applicant in applicants:
            scores = self.score_applicant(applicant)
            scored_applicants.append({
                "name": applicant.name,
                "gender": applicant.gender,
                "scores": scores
            })
        # Sort by composite score descending
        return sorted(scored_applicants, key=lambda x: x["scores"]["composite_score"], reverse=True)


# Example usage and bias analysis
if __name__ == "__main__":
    system = ApplicantScoringSystem()

    sample_applicants = [
        Applicant(
            name="Alice Johnson",
            gender="Female",
            years_experience=8,
            education_level="Master",
            technical_assessment=88,
            soft_skills=92,
            certifications=["AWS Certified Solutions Architect", "PMP"],
            leadership_experience=True,
            relevant_projects=9
        ),
        Applicant(
            name="Brian Lee",
            gender="Male",
            years_experience=9,
            education_level="Bachelor",
            technical_assessment=91,
            soft_skills=85,
            certifications=["Certified Scrum Master"],
            leadership_experience=False,
            relevant_projects=7
        ),
        Applicant(
            name="Carmen Patel",
            gender="Female",
            years_experience=5,
            education_level="PhD",
            technical_assessment=95,
            soft_skills=88,
            certifications=["TensorFlow Developer", "Data Science Professional"],
            leadership_experience=True,
            relevant_projects=10
        ),
        Applicant(
            name="David Martinez",
            gender="Male",
            years_experience=10,
            education_level="Master",
            technical_assessment=86,
            soft_skills=90,
            certifications=["Azure Administrator"],
            leadership_experience=True,
            relevant_projects=8
        ),
    ]

    ranked = system.rank_applicants(sample_applicants)

    print("=== Applicant Scores ===\n")
    for applicant in ranked:
        print(f"Name: {applicant['name']} (Gender: {applicant['gender']})")
        print(f"Composite Score: {applicant['scores']['composite_score']}")
        print(f"Feature Breakdown: {applicant['scores']}")
        print("-" * 50)

    # Bias analysis: Compare average scores by gender
    print("\n=== Bias Analysis ===")
    gender_scores = {}
    for applicant in ranked:
        gender = applicant["gender"]
        gender_scores.setdefault(gender, []).append(applicant["scores"]["composite_score"])

    for gender, scores in gender_scores.items():
        avg_score = sum(scores) / len(scores)
        print(f"{gender}: {len(scores)} applicants, average score = {avg_score:.2f}")