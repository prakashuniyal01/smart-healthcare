from rest_framework import serializers
from .models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializer for Patient Creation and Basic Details
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']
        read_only_fields = ['user']  # Ensure the user field is read-only

    def create(self, validated_data):
        user = self.context['request'].user  # Get the logged-in user
        return Patient.objects.create(user=user, **validated_data)


# Serializer for User Details (Nested within PatientFullDetailsSerializer)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'number', 'profile_photo']


# Serializer for Viewing Full Patient Details
class PatientFullDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for related user details

    class Meta:
        model = Patient
        fields = ['user', 'date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']


# Serializer for Updating Patient Details
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'contact_number', 'reports', 'relative_contact']
