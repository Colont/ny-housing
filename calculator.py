import numpy as np

class AffordabilityCalculator:
    def __init__(self, annual_income, credit_score, down_payment):
        self.annual_income = annual_income
        self.credit_score = credit_score
        self.down_payment = down_payment

    def get_interest_rate(self):
        # Define interest rates based on credit score (simplified assumption)
        if self.credit_score >= 760:
            return 0.045  # 4.5% for excellent credit
        elif self.credit_score >= 700:
            return 0.05   # 5.0% for good credit
        elif self.credit_score >= 650:
            return 0.06   # 6.0% for fair credit
        else:
            return 0.07   # 7.0% for poor credit

    def calculate_max_affordable_price(self):
        interest_rate = self.get_interest_rate()

        # Mortgage parameters
        loan_term_years = 30
        monthly_interest_rate = interest_rate / 12
        num_payments = loan_term_years * 12

        # Maximum Monthly Payment (28% of gross monthly income)
        max_monthly_payment = 0.28 * (self.annual_income / 12)

        # Calculate the maximum loan amount using the annuity formula
        loan_amount = max_monthly_payment * (1 - (1 + monthly_interest_rate) ** -num_payments) / monthly_interest_rate

        # Calculate the total house price the user can afford
        max_house_price = loan_amount + self.down_payment

        return round(max_house_price, 2)
