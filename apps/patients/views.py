# patients/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer, PatientFullDetailsSerializer, PatientUpdateSerializer

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user role is 'patient'
        if request.user.role != 'patient':
            return Response({"error": "Only patients can create a profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve the patient's profile
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)
        

class PatientFullDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure the user is a patient
        if request.user.role != 'patient':
            return Response({"error": "Only patients can access this information."}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Get the patient details
            patient = Patient.objects.get(user=request.user)
            serializer = PatientFullDetailsSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)

class UpdatePatientDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Ensure the user is a patient
        if request.user.role != 'patient':
            return Response({"error": "Only patients can update their details."}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the patient instance
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate the data
        serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient details updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




