from rest_framework import serializers
from .models import Appointment, Leave
from django.utils.timezone import now
from datetime import datetime, timedelta

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'start_time', 'end_time', 'status']
        read_only_fields = ['id', 'patient', 'status']  # `patient` is read-only because it will be set automatically

    def validate(self, data):
        # Ensure the date is not in the past
        if data['date'] < datetime.now().date():
            raise serializers.ValidationError("Appointments cannot be booked for past dates.")

        # Ensure start_time is before end_time
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")

        # Ensure the doctor is not on leave for the given date
        doctor = data['doctor']
        if Leave.objects.filter(doctor=doctor, date=data['date']).exists():
            raise serializers.ValidationError("The doctor is on leave on the selected date.")

        # Ensure the slot is not already booked
        if Appointment.objects.filter(
            doctor=doctor,
            date=data['date'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
            status="confirmed"
        ).exists():
            raise serializers.ValidationError("This time slot is already booked.")

        return data

    def create(self, validated_data):
        # Set the patient as the logged-in user
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['id', 'doctor', 'date', 'reason', 'is_approved']
        read_only_fields = ['id', 'is_approved']

    def validate(self, data):
        # Check if leave date is in the past
        if data['date'] < now().date():
            raise serializers.ValidationError("Leave cannot be scheduled for past dates.")
        return data
