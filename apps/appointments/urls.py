from django.urls import path
from .views import AppointmentCreateView, AppointmentUpdateView, LeaveCreateView

urlpatterns = [
    # Appointment URLs
    path('appointments/', AppointmentCreateView.as_view(), name='create_appointment'),  # Book an appointment
    path('appointments/<uuid:pk>/', AppointmentUpdateView.as_view(), name='update_appointment'),  # Update appointment status

    # Leave URLs
    path('leaves/', LeaveCreateView.as_view(), name='create_leave'),  # Schedule a leave
]
