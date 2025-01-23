# views.py (in doctors app)

from rest_framework import status, permissions, viewsets,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DoctorSerializer,DoctorSerializerGet, DoctorUpdateSerializer, SpecializationSerializer , WeeklyScheduleSerializer, DoctorLeaveSerializer, DoctorSerializerAll
from .models import Doctor ,Specialization ,WeeklySchedule, DoctorLeave
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound

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
        
class WeeklyScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WeeklyScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedules = serializer.create(serializer.validated_data)
            response_data = WeeklyScheduleSerializer(schedules, many=True).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLeaveView(generics.ListCreateAPIView):
    """
    Handles Doctor Leaves
    GET: View all leaves.
    POST: Add a new leave.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorLeaveSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return DoctorLeave.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)  
        

class DoctorListView(APIView):
    """
    Retrieve a list of all doctors with full details.
    """
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
        
        
class DoctorDetailViewall(APIView):
    def get(self, request, doctor_id=None):
        """
        Fetch detailed doctor information.
        If `doctor_id` is provided, fetch specific doctor details;
        otherwise, fetch details of all doctors.
        """
        if doctor_id:
            try:
                doctor = Doctor.objects.get(user_id=doctor_id)
                serializer = DoctorSerializerAll(doctor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Doctor.DoesNotExist:
                return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializerAll(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)