from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

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
    date = models.DateField(default=timezone.now)  # Specific date for the schedule
    day_of_week = models.IntegerField()  # 0: Monday, 6: Sunday
    start_time = models.TimeField(default="10:00:00")
    end_time = models.TimeField(default="18:00:00")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date')  # Ensures one schedule per date per doctor

    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.date} (Day {self.day_of_week})"

    @classmethod
    def generate_weekly_schedule(cls, doctor, start_date=None, end_date=None):
        """
        Generate a weekly schedule for the given doctor from the given start_date to end_date.
        """
        if not start_date:
            start_date = datetime.now().date()  # Default to today
        if not end_date:
            end_date = start_date + timedelta(days=(6 - start_date.weekday()))  # End of the week

        schedules = []
        for single_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
            day_of_week = single_date.weekday()  # Get the day of the week (0: Monday, 6: Sunday)

            # Skip Sundays (or any other inactive days if needed)
            if day_of_week == 6:
                continue

            # Use update_or_create to handle existing schedules
            schedule, created = cls.objects.update_or_create(
                doctor=doctor,
                date=single_date,
                defaults={
                    "day_of_week": day_of_week,
                    "start_time": "10:00:00",  # Default start time
                    "end_time": "18:00:00",    # Default end time
                    "is_active": True,
                },
            )
            schedules.append(schedule)

        return schedules



class DoctorLeave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="leaves")
    leave_date = models.DateField(unique=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.leave_date}"