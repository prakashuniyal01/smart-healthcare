# patients/urls.py
from django.urls import path
from .views import PatientProfileView, PatientFullDetailsView, UpdatePatientDetailsView

urlpatterns = [
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('details/', PatientFullDetailsView.as_view(), name='patient-details'),
    path('update/', UpdatePatientDetailsView.as_view(), name='update-patient-details'),
]

