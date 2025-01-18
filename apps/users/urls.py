from django.urls import path
from .views import UserRegistrationView, VerifyOTPView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
