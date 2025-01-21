# patients/serializers.py
from rest_framework import serializers
from .models import Patient
from django.contrib.auth import get_user_model
User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        return Patient.objects.create(user=user, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'number', 'profile_photo']

class PatientFullDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for user details

    class Meta:
        model = Patient
        fields = ['id','user', 'date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']
        
        

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']