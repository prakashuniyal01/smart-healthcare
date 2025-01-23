from rest_framework import serializers
from .models import Doctor, Specialization  , WeeklySchedule, DoctorLeave
from datetime import datetime, timedelta, date
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
        fields = [ 'doctor', 'date', 'day_of_week', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['id', 'day_of_week']

    def validate(self, data):
        doctor = data.get('doctor')
        date = data.get('date')

        # Check if a schedule for this doctor and date already exists
        if WeeklySchedule.objects.filter(doctor=doctor, date=date).exists():
            raise serializers.ValidationError("A schedule already exists for this doctor on this date.")
        
        return data


    def create(self, validated_data):
        doctor = validated_data['doctor']
        start_date = validated_data.pop('start_date', datetime.date())
        end_date = validated_data.pop('end_date', start_date + timedelta(days=6))

        # Generate schedule for the doctor from start_date to end_date
        schedules = WeeklySchedule.generate_weekly_schedule(
            doctor, start_date=start_date, end_date=end_date
        )
        
        # Serialize the created or updated schedules
        return schedules

    
class DoctorLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLeave
        fields = ['id', 'doctor', 'leave_date', 'reason']
        read_only_fields = ['id', 'doctor']      
        

class DoctorSerializerAll(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # To include detailed user information
    specialization = SpecializationSerializer()  # Nested specialization data
    weekly_schedule = WeeklyScheduleSerializer(many=True, source='weekly_schedules')  # Nested weekly schedule data
    leaves = DoctorLeaveSerializer(many=True)  # Nested doctor leave data

    class Meta:
        model = Doctor
        fields = [
            'user', 'specialization', 'degree', 'license_number',
            'years_of_experience', 'consultation_fee', 'profile_description',
            'max_patients_per_day', 'is_active', 'weekly_schedule', 'leaves'
        ]

    def get_user(self, obj):
        user = obj.user
        return {
            'id': str(user.id),
            'full_name': user.full_name,
            'email': user.email,
            'profile_photo': user.profile_photo.url if user.profile_photo else None
        }

    def to_representation(self, instance):
        """
        Add custom logic here if you need to transform or format the data further.
        """
        representation = super().to_representation(instance)
        return representation
