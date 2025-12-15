from django import forms


class PredictForm(forms.Form):
    annual_income = forms.FloatField(label="Annual Income", required=True)
    debt_to_income_ratio = forms.FloatField(
        label="Debt-to-Income Ratio", required=False, min_value=0, max_value=1
    )
    credit_score = forms.IntegerField(label="Credit Score", required=False)
    loan_amount = forms.FloatField(label="Loan Amount", required=True)
    interest_rate = forms.FloatField(label="Interest Rate", required=False)

    gender = forms.ChoiceField(
        choices=[("", "-- Select --"), ("Female", "Female"), ("Male", "Male"), ("Other", "Other")],
        required=False,
    )
    marital_status = forms.ChoiceField(
        choices=[
            ("", "-- Select --"),
            ("Single", "Single"),
            ("Married", "Married"),
            ("Divorced", "Divorced"),
            ("Widowed", "Widowed"),
        ],
        required=False,
    )
    education_level = forms.ChoiceField(
        choices=[
            ("", "-- Select --"),
            ("High School", "High School"),
            ("Bachelor's", "Bachelor's"),
            ("Master's", "Master's"),
            ("PhD", "PhD"),
            ("Other", "Other"),
        ],
        required=False,
    )
    employment_status = forms.ChoiceField(
        choices=[
            ("", "-- Select --"),
            ("Self-employed", "Self-employed"),
            ("Employed", "Employed"),
            ("Unemployed", "Unemployed"),
            ("Retired", "Retired"),
            ("Student", "Student"),
        ],
        required=False,
    )
    loan_purpose = forms.ChoiceField(
        choices=[
            ("", "-- Select --"),
            ("Other", "Other"),
            ("Debt consolidation", "Debt consolidation"),
            ("Home", "Home"),
            ("Education", "Education"),
            ("Vacation", "Vacation"),
            ("Car", "Car"),
            ("Medical", "Medical"),
            ("Business", "Business"),
        ],
        required=False,
    )
    grade_subgrade = forms.ChoiceField(
        choices=[
            ("", "-- Select --"),
            *[(f"{g}{i}", f"{g}{i}") for g in "ABCDEF" for i in range(1, 6)],
        ],
        required=False,
    )
