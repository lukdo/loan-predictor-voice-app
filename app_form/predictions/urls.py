from django.urls import path
from .views import PredictView, PredictionRecordDetailView

urlpatterns = [
    path("", PredictView.as_view(), name="predict_form"),
    path("detail/<int:pk>/", PredictionRecordDetailView.as_view(), name="detail"),
]
