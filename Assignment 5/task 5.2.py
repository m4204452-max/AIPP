# task 5.2.py - Loan Approval System
import json
from typing import Dict, Optional, Tuple
from datetime import datetime

class LoanApprovalSystem:
    """
    Loan approval system that evaluates loan applications based on financial criteria.
    """
    
    def __init__(self):
        self.applications = []
        self.min_credit_score = 650
        self.min_income_ratio = 0.3  # Debt-to-income ratio threshold
        self.max_loan_amount = 500000
        self.min_employment_years = 2
    
    def calculate_debt_to_income_ratio(self, monthly_income: float, monthly_debt: float) -> float:
        """Calculate debt-to-income ratio"""
        if monthly_income == 0:
            return float('inf')
        return monthly_debt / monthly_income
    
    def calculate_credit_score_adjustment(self, credit_score: int) -> float:
        """Calculate credit score adjustment factor"""
        if credit_score >= 750:
            return 1.0
        elif credit_score >= 700:
            return 0.9
        elif credit_score >= 650:
            return 0.8
        else:
            return 0.0
    
    def evaluate_application(self, name: str, gender: str, age: int, 
                            monthly_income: float, credit_score: int,
                            loan_amount: float, employment_years: float,
                            monthly_debt: float = 0.0) -> Tuple[bool, str, Dict]:
        """
        Evaluate loan application based on financial criteria.
        
        Args:
            name: Applicant's name
            gender: Applicant's gender
            age: Applicant's age
            monthly_income: Monthly income
            credit_score: Credit score
            loan_amount: Requested loan amount
            employment_years: Years of employment
            monthly_debt: Existing monthly debt payments
        
        Returns:
            Tuple of (approved, reason, details)
        """
        details = {
            'name': name,
            'gender': gender,
            'age': age,
            'monthly_income': monthly_income,
            'credit_score': credit_score,
            'loan_amount': loan_amount,
            'employment_years': employment_years,
            'monthly_debt': monthly_debt,
            'evaluated_at': datetime.now().isoformat()
        }
        
        # Check age requirement
        if age < 18:
            return False, "Applicant must be at least 18 years old", details
        
        # Check credit score
        if credit_score < self.min_credit_score:
            return False, f"Credit score {credit_score} is below minimum {self.min_credit_score}", details
        
        # Check loan amount
        if loan_amount > self.max_loan_amount:
            return False, f"Loan amount {loan_amount} exceeds maximum {self.max_loan_amount}", details
        
        # Check employment history
        if employment_years < self.min_employment_years:
            return False, f"Employment history {employment_years} years is below minimum {self.min_employment_years} years", details
        
        # Calculate debt-to-income ratio
        monthly_payment = loan_amount * 0.01  # Simplified: 1% monthly payment
        total_monthly_debt = monthly_debt + monthly_payment
        dti_ratio = self.calculate_debt_to_income_ratio(monthly_income, total_monthly_debt)
        
        if dti_ratio > self.min_income_ratio:
            return False, f"Debt-to-income ratio {dti_ratio:.2f} exceeds threshold {self.min_income_ratio}", details
        
        # Calculate credit score adjustment
        credit_adjustment = self.calculate_credit_score_adjustment(credit_score)
        
        # Calculate income adequacy
        required_monthly_income = loan_amount * 0.02  # Simplified requirement
        income_adequate = monthly_income >= required_monthly_income
        
        if not income_adequate:
            return False, f"Monthly income {monthly_income} is insufficient for loan amount {loan_amount}", details
        
        # All checks passed
        details['approval_score'] = credit_adjustment * (1 - dti_ratio)
        return True, "Loan approved", details
    
    def process_application(self, application_data: Dict) -> Dict:
        """Process a loan application"""
        result = self.evaluate_application(
            name=application_data.get('name'),
            gender=application_data.get('gender'),
            age=application_data.get('age'),
            monthly_income=application_data.get('monthly_income'),
            credit_score=application_data.get('credit_score'),
            loan_amount=application_data.get('loan_amount'),
            employment_years=application_data.get('employment_years'),
            monthly_debt=application_data.get('monthly_debt', 0.0)
        )
        
        approved, reason, details = result
        application_result = {
            'approved': approved,
            'reason': reason,
            'details': details
        }
        
        self.applications.append(application_result)
        return application_result


# Example usage and testing
if __name__ == "__main__":
    system = LoanApprovalSystem()
    
    # Test cases with different genders and names
    test_applications = [
        {
            'name': 'John Smith',
            'gender': 'Male',
            'age': 35,
            'monthly_income': 5000,
            'credit_score': 720,
            'loan_amount': 100000,
            'employment_years': 5,
            'monthly_debt': 500
        },
        {
            'name': 'Sarah Johnson',
            'gender': 'Female',
            'age': 32,
            'monthly_income': 5000,
            'credit_score': 720,
            'loan_amount': 100000,
            'employment_years': 5,
            'monthly_debt': 500
        },
        {
            'name': 'Michael Chen',
            'gender': 'Male',
            'age': 28,
            'monthly_income': 4500,
            'credit_score': 680,
            'loan_amount': 80000,
            'employment_years': 3,
            'monthly_debt': 300
        },
        {
            'name': 'Priya Patel',
            'gender': 'Female',
            'age': 30,
            'monthly_income': 4500,
            'credit_score': 680,
            'loan_amount': 80000,
            'employment_years': 3,
            'monthly_debt': 300
        },
        {
            'name': 'David Williams',
            'gender': 'Male',
            'age': 25,
            'monthly_income': 3000,
            'credit_score': 600,
            'loan_amount': 50000,
            'employment_years': 1,
            'monthly_debt': 200
        },
        {
            'name': 'Emily Davis',
            'gender': 'Female',
            'age': 27,
            'monthly_income': 3000,
            'credit_score': 600,
            'loan_amount': 50000,
            'employment_years': 1,
            'monthly_debt': 200
        }
    ]
    
    print("=== Loan Approval System Test ===\n")
    
    for app in test_applications:
        result = system.process_application(app)
        status = "APPROVED" if result['approved'] else "REJECTED"
        print(f"Applicant: {app['name']} ({app['gender']})")
        print(f"Status: {status}")
        print(f"Reason: {result['reason']}")
        print(f"Credit Score: {app['credit_score']}, Income: ${app['monthly_income']}")
        print("-" * 50)
    
    # Analyze approval rates by gender
    print("\n=== Approval Rate Analysis by Gender ===")
    male_apps = [a for a in system.applications if a['details']['gender'] == 'Male']
    female_apps = [a for a in system.applications if a['details']['gender'] == 'Female']
    
    male_approved = sum(1 for a in male_apps if a['approved'])
    female_approved = sum(1 for a in female_apps if a['approved'])
    
    male_rate = (male_approved / len(male_apps) * 100) if male_apps else 0
    female_rate = (female_approved / len(female_apps) * 100) if female_apps else 0
    
    print(f"Male applicants: {male_approved}/{len(male_apps)} approved ({male_rate:.1f}%)")
    print(f"Female applicants: {female_approved}/{len(female_apps)} approved ({female_rate:.1f}%)")