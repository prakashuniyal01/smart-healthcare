from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'full_name', 'role', 'is_active', 'is_staff', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    
    # Fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'number', 'profile_photo')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'number', 'profile_photo', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at')

# Register your custom User model with the admin site
admin.site.register(User, CustomUserAdmin)
