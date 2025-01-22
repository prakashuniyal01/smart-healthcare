from rest_framework import serializers
from .models import Doctor, Specialization  , WeeklySchedule, DoctorLeave
from django.contrib.auth import get_user_model

User = get_user_model()

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'description']



class DoctorSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    specialization = serializers.CharField()  # Accept specialization name as a string

    class Meta:
        model = Doctor
        fields = [
            'user_id', 'specialization', 'degree', 'license_number',
            'years_of_experience', 'consultation_fee', 'profile_description',
            'max_patients_per_day', 'is_active'
        ]

    def create(self, validated_data):
        # Extract and handle specialization
        specialization_name = validated_data.pop('specialization')
        specialization, _ = Specialization.objects.get_or_create(name=specialization_name)

        user = self.context['request'].user  # User making the request (assumes it's a doctor)
        doctor = Doctor.objects.create(
            user=user,
            specialization=specialization,
            **validated_data
        )
        return doctor

class DoctorSerializerGet(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    specialization = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'user', 'specialization', 'degree', 'license_number',
            'years_of_experience', 'consultation_fee', 'profile_description',
            'max_patients_per_day', 'is_active'
        ]

    def get_user(self, obj):
        user = obj.user
        return {
            'full_name': user.full_name,
            'email': user.email,
            'profile_photo': user.profile_photo.url if user.profile_photo else None
        }

    def get_specialization(self, obj):
        specialization = obj.specialization
        return {
            'name': specialization.name,
            'description': specialization.description
        }

class DoctorUpdateSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(required=False)  # Accept specialization name as a string

    class Meta:
        model = Doctor
        fields = [
            'specialization', 'degree', 'license_number', 'years_of_experience',
            'consultation_fee', 'profile_description', 'max_patients_per_day'
        ]

    def update(self, instance, validated_data):
        # Handle specialization
        specialization_name = validated_data.pop('specialization', None)
        if specialization_name:
            specialization, _ = Specialization.objects.get_or_create(name=specialization_name)
            instance.specialization = specialization

        # Update other fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
   
        
class WeeklyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySchedule
        fields = ['id', 'doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['id', 'doctor']

    def validate(self, data):
        # Ensure start_time is before end_time
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data


class DoctorLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLeave
        fields = ['id', 'doctor', 'leave_date', 'reason']
        read_only_fields = ['id', 'doctor']      
        

class DoctorSerializerAll(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    specialization = SpecializationSerializer()
    weekly_schedule = WeeklyScheduleSerializer(many=True)
    leaves = DoctorLeaveSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user_id', 'specialization', 'degree', 'license_number',
                  'years_of_experience', 'consultation_fee', 'profile_description',
                  'max_patients_per_day', 'is_active', 'weekly_schedule', 'leaves']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # You can add any additional custom logic here if needed
        return representation