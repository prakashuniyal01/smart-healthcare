# admin.py (in patients app)

from django.contrib import admin
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'relative_contact', 'date_of_birth', 'gender', 'reports')
    search_fields = ['user__full_name', 'contact_number']
    list_filter = ['gender']

admin.site.register(Patient, PatientAdmin)
