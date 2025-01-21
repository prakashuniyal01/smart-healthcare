# admin.py (in doctors app)

from django.contrib import admin
from .models import Doctor, Specialization

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'degree', 'license_number', 'years_of_experience', 'consultation_fee', 'max_patients_per_day', 'is_active')
    search_fields = ['user__full_name', 'specialization__name', 'license_number']
    list_filter = ['is_active', 'specialization']


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Ensure 'description' exists as a field
    

# Register the models to be available in the admin panel
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specialization, SpecializationAdmin)
