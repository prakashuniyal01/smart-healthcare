from rest_framework import serializers
from .models import User
from .email_service import send_otp_email
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            full_name=validated_data.get('full_name'),
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            password=validated_data['password'],
            role=validated_data.get('role', 'patient')
        )
        # Generate OTP and send it to the user's email
        user.generate_otp()
        send_otp_email(user.email, user.otp)
        return user


# login 
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials.')

        return {'user': user}

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
