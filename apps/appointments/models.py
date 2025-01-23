import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')  # Ensure no overlapping appointments

    def __str__(self):
        return f"Appointment: {self.patient.full_name} with {self.doctor.full_name} on {self.date}"

class Leave(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_leaves')
    date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date')

    def __str__(self):
        return f"Leave: {self.doctor.full_name} on {self.date}"
