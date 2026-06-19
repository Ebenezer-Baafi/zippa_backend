from django.urls import path
from .views import FareEstimationView

urlpatterns = [
    path('fare-estimate/', FareEstimationView.as_view(), name='fare-estimate'),
]