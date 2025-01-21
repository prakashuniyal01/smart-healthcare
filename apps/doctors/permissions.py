# permissions.py (in doctors app)

from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'
