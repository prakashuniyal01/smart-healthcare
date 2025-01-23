from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .models import Appointment, Leave
from .serializers import AppointmentSerializer, LeaveSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import PermissionDenied

class AppointmentCreateView(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure only patients can create appointments
        if self.request.user.role != "patient":
            raise PermissionDenied("You are not authorized to book an appointment.")
        serializer.save()

class AppointmentUpdateView(generics.UpdateAPIView):
    """
    Allows doctors to confirm or cancel appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'doctor':
            raise permissions.PermissionDenied("Only doctors can update appointments.")
        return Appointment.objects.filter(doctor=user)

class LeaveCreateView(generics.CreateAPIView):
    """
    Allows doctors to schedule leaves.
    """
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'doctor':
            raise permissions.PermissionDenied("Only doctors can schedule leaves.")
        serializer.save(doctor=user)
