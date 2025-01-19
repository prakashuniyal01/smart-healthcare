from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.utils.timezone import now
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

# register 
class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully. OTP has been sent to your email.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# varify 
class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.otp == otp and user.otp_expiration > now():
                user.email_verified = True
                user.otp = None  # Clear OTP after successful verification
                user.otp_expiration = None
                user.save()
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

# login 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserLoginSerializer

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_tokens_for_user(user)

            user_data = {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'role': user.role,
                'profile_photo': user.profile_photo.url if user.profile_photo else None,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
            }

            return Response({
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
