# serializers.py
from rest_framework import serializers
from .models import User,PasswordReset
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'number', 'profile_photo']
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name','role', 'number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            role=validated_data['role'],
            number=validated_data.get('number', None),
        )
        return user
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        data['user'] = user
        return data
    
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'number', 'profile_photo']  # Include email for updating

    def update(self, instance, validated_data):
        # Check if email has changed and is unique
        new_email = validated_data.get('email', instance.email)
        if new_email != instance.email:
            if User.objects.filter(email=new_email).exists():
                raise serializers.ValidationError("This email is already taken.")
            instance.email = new_email
        
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.number = validated_data.get('number', instance.number)
        if 'profile_photo' in validated_data:
            instance.profile_photo = validated_data['profile_photo']
        
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request'].user  # Get the current user from the request context
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if old password is correct
        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")
        
        # Ensure new password and confirm password match
        if new_password != confirm_password:
            raise ValidationError("New passwords do not match.")
        
        return attrs
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if the email exists in the database."""
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        """Validate the OTP and check if it's expired."""
        try:
            password_reset = PasswordReset.objects.get(user__email=data['email'], otp=data['otp'])
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")
        if password_reset.is_expired():
            raise serializers.ValidationError("OTP has expired.")
        return data
    
