from django.db import models


class PredictionRecord(models.Model):
    name_surname = models.CharField(max_length=200, null=True, blank=True)
    annual_income = models.FloatField()
    debt_to_income_ratio = models.FloatField(null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)
    loan_amount = models.FloatField()
    interest_rate = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    education_level = models.CharField(max_length=50, null=True, blank=True)
    employment_status = models.CharField(max_length=50, null=True, blank=True)
    loan_purpose = models.CharField(max_length=50, null=True, blank=True)
    grade_subgrade = models.CharField(max_length=10, null=True, blank=True)
    approved = models.BooleanField()
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_surname or 'Unknown'} - Prediction ({'Approved' if self.approved else 'Rejected'}) - {self.probability}%"
