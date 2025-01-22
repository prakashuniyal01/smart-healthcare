from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Specialization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,  # Use the User's primary key as Doctor's primary key
        related_name='doctor_profile'
    )
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    degree = models.CharField(max_length=50, default="Not Specified")
    license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.IntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    profile_description = models.TextField(default="Not Specified")
    max_patients_per_day = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.full_name} ({self.specialization.name})"


class WeeklySchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="weekly_schedules")
    day_of_week = models.IntegerField()  # 0: Sunday, 6: Saturday
    start_time = models.TimeField(default="10:00:00")
    end_time = models.TimeField(default="18:00:00")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week')  # Ensure one schedule per day per doctor

    def __str__(self):
        return f"{self.doctor.user.full_name} - Day {self.day_of_week}"


class DoctorLeave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="leaves")
    leave_date = models.DateField(unique=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.leave_date}"