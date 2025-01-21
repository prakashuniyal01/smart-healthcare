# patients/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patients_profile')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    contact_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    reports = models.BinaryField(null=True, blank=True)  # To store files like PDF
    relative_contact = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"
