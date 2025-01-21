# urls.py (in doctors app)

from django.urls import path
from .views import DoctorProfileCreateView, DoctorDetailView, DoctorUpdateView, SpecializationView, WeeklyScheduleViewSet, DoctorLeaveViewSet

urlpatterns = [
    path('specializations/', SpecializationView.as_view(), name='specializations-list'),
    path('doctor/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('profile/', DoctorProfileCreateView.as_view(), name='create-doctor-profile'),
    path('update/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('weekly_schedule/create/', WeeklyScheduleViewSet.as_view(), name='create_weekly_schedule'),
    path('doctor_leaves/apply/', DoctorLeaveViewSet.as_view(), name='apply_doctor_leave'),
]