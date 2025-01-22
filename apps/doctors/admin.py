from django.contrib import admin
from .models import Doctor, Specialization, WeeklySchedule, DoctorLeave

# Doctor Admin Configuration
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'degree', 'license_number', 'years_of_experience', 'consultation_fee', 'max_patients_per_day', 'is_active')
    search_fields = ['user__full_name', 'specialization__name', 'license_number']
    list_filter = ['is_active', 'specialization', 'years_of_experience']
    ordering = ('user__full_name',)  # Ordering by full name of the doctor

    # Fieldsets for detailed view in form
    fieldsets = (
        (None, {
            'fields': ('user', 'specialization', 'degree', 'license_number', 'years_of_experience')
        }),
        ('Consultation Details', {
            'fields': ('consultation_fee', 'max_patients_per_day', 'is_active')
        }),
        ('Profile Description', {
            'fields': ('profile_description',)
        }),
    )
    readonly_fields = ('user', 'license_number')  # Make some fields read-only

    # Adding actions to deactivate or activate multiple doctors at once
    actions = ['activate_doctors', 'deactivate_doctors']

    def activate_doctors(self, request, queryset):
        queryset.update(is_active=True)
    activate_doctors.short_description = "Activate selected doctors"

    def deactivate_doctors(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_doctors.short_description = "Deactivate selected doctors"


# Specialization Admin Configuration
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']
    ordering = ('name',)  # Orders by specialization name
    
    # Adding list filters for better UI experience
    list_filter = ('name',)

    # Allow sorting by name for improved UX
    ordering = ('name',)

    # Adding a custom action to delete all specializations (just as an example)
    actions = ['delete_all_specializations']

    def delete_all_specializations(self, request, queryset):
        queryset.delete()
    delete_all_specializations.short_description = "Delete selected specializations"


# Registering the models in the admin panel
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Specialization, SpecializationAdmin)

# Registering Weekly Schedule and Doctor Leave models with the same concept (example)
@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_active')
    search_fields = ['doctor__user__full_name']
    list_filter = ['is_active', 'day_of_week']
    ordering = ('doctor', 'day_of_week')

@admin.register(DoctorLeave)
class DoctorLeaveAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'leave_date', 'reason')
    search_fields = ['doctor__user__full_name', 'reason']
    list_filter = ['leave_date']
    ordering = ('doctor', 'leave_date')
