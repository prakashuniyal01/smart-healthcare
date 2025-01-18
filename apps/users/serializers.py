from rest_framework import serializers
from .models import User
from .email_service import send_otp_email

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        # Generate OTP and send it to the user's email
        user.generate_otp()
        send_otp_email(user.email, user.otp)
        return user
