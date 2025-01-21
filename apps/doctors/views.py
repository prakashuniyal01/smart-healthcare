# views.py (in doctors app)

from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DoctorSerializer,DoctorSerializerGet, DoctorUpdateSerializer, SpecializationSerializer, WeeklyScheduleSerializer, DoctorLeaveSerializer
from .models import Doctor ,Specialization,WeeklySchedule, DoctorLeave
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsDoctor

class DoctorProfileCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != 'doctor':
            return Response(
                {"detail": "You must be a doctor to create a doctor profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = DoctorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor profile created successfully',
                'doctor': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Get doctor object based on user_id
            doctor = Doctor.objects.get(user_id=request.user.id)
            serializer = DoctorSerializerGet(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)


class DoctorUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user_id=request.user.id)
        
        # Check if the logged-in user is a doctor (if the role is doctor)
        if doctor is None or request.user.role != 'doctor':
            return Response({"error": "You do not have permission to update this information."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_doctor = serializer.save()
            return Response({
                'message': 'Doctor details updated successfully',
                'doctor': {
                    'specialization': updated_doctor.specialization.name,
                    'degree': updated_doctor.degree,
                    'license_number': updated_doctor.license_number,
                    'years_of_experience': updated_doctor.years_of_experience,
                    'consultation_fee': updated_doctor.consultation_fee,
                    'profile_description': updated_doctor.profile_description,
                    'max_patients_per_day': updated_doctor.max_patients_per_day
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SpecializationView(APIView):
    def get(self, request):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=200)
        
class WeeklyScheduleViewSet(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]  # Ensure only doctors can access

    def post(self, request):
        # Allow doctors to create their weekly schedule
        serializer = WeeklyScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user.doctor_profile)  # Associate the schedule with the logged-in doctor
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLeaveViewSet(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]  # Ensure only doctors can access

    def post(self, request):
        # Allow doctors to apply for leaves
        serializer = DoctorLeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user.doctor_profile)  # Associate the leave with the logged-in doctor
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        
        
        
        
        