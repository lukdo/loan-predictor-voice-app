from django.shortcuts import render
from django.views import View
from .services.api_client import predict
from .predict_form import PredictForm
from .models import PredictionRecord
from django.views.generic import ListView
from django.views.generic import DetailView


class PredictView(View):
    template_name = "predictions/predict.html"

    def get(self, request):
        form = PredictForm()
        grades = [
            "A1", "A2", "A3", "A4", "A5",
            "B1", "B2", "B3", "B4", "B5",
            "C1", "C2", "C3", "C4", "C5",
            "D1", "D2", "D3", "D4", "D5",
            "E1", "E2", "E3", "E4", "E5",
            "F1", "F2", "F3", "F4", "F5",
        ]
        predictions = PredictionRecord.objects.all().order_by("-created_at")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "form_data": {},
                "message": None,
                "grades": grades,
                "predictions": predictions,
            },
        )

    def post(self, request):
        form = PredictForm(request.POST)
        message = None
        prediction_result = None
        errors = []

        if form.is_valid():
            payload = form.cleaned_data
            api_result = predict(payload)

            if api_result and "approved" in api_result and "probability" in api_result:
                prediction_result = {
                    "approved": api_result["approved"],
                    "probability": round(api_result["probability"], 1),
                }
                message = "Prediction from API successful."
            else:
                try:
                    income = float(payload.get("annual_income", 0))
                    loan = float(payload.get("loan_amount", 0))
                    if income > 0 and loan > 0 and income / loan > 2:
                        approved = True
                        probability = 0.85
                    else:
                        approved = False
                        probability = 0.35
                    prediction_result = {
                        "approved": approved,
                        "probability": round(probability, 1),
                    }
                    message = "Fallback prediction logic applied."
                except ValueError:
                    errors.append("Invalid numeric input. Please check your values.")

            # Save to database
            if prediction_result:
                PredictionRecord.objects.create(
                    name_surname=request.POST.get("name_surname") or payload.get("name_surname"),
                    annual_income=payload.get("annual_income"),
                    debt_to_income_ratio=payload.get("debt_to_income_ratio"),
                    credit_score=payload.get("credit_score"),
                    loan_amount=payload.get("loan_amount"),
                    interest_rate=payload.get("interest_rate"),
                    gender=payload.get("gender"),
                    marital_status=payload.get("marital_status"),
                    education_level=payload.get("education_level"),
                    employment_status=payload.get("employment_status"),
                    loan_purpose=payload.get("loan_purpose"),
                    grade_subgrade=payload.get("grade_subgrade"),
                    approved=prediction_result["approved"],
                    probability=prediction_result["probability"],
                )

        else:
            errors = [f"{field}: {error}" for field, error_list in form.errors.items() for error in error_list]

        context = {
            "form": form,
            "form_data": request.POST,
            "message": message,
            "prediction_result": prediction_result,
            "errors": errors,
        }
        grades = [
            "A1", "A2", "A3", "A4", "A5",
            "B1", "B2", "B3", "B4", "B5",
            "C1", "C2", "C3", "C4", "C5",
            "D1", "D2", "D3", "D4", "D5",
            "E1", "E2", "E3", "E4", "E5",
            "F1", "F2", "F3", "F4", "F5",
        ]
        context["grades"] = grades
        # Include all predictions in context for display
        context["predictions"] = PredictionRecord.objects.all().order_by("-created_at")
        return render(request, "predictions/predict.html", context)



class PredictionListView(ListView):
   model = PredictionRecord
   template_name = "predictions/predict.html"
   context_object_name = "predictions"



class PredictionRecordDetailView(DetailView):
   model = PredictionRecord
   template_name = "predictions/prediction_detail.html"
   context_object_name = "record"
