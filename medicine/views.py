from django.http import Http404
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Owner, Pharmacy
from drf_spectacular.utils import extend_schema
from accounts.authentication import PharmacyJWTAuthentication
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsOwnerNotStuff

class MedicineCreateReadView(APIView):
    authentication_classes = [PharmacyJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MedicineSerializer
    
    def get(self, request):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        medicines = Medicine.objects.filter(pharmacy=pharmacy).select_related('pharmacy')
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
           
    def post(self,request):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data
        data['pharmacy'] = pharmacy.id

        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicineRetrieveUpdateDestroy(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicineSerializer

    def get_medicine(self, pk, pharmacy):
        try:
            medicine = Medicine.objects.get(id=pk)
        except Medicine.DoesNotExist:
            return None, Response(
                {"error": "Medicine not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if medicine.pharmacy != pharmacy:
            return None, Response(
                {"error": "You do not have permission to access this medicine"},
                status=status.HTTP_403_FORBIDDEN
            )
        return medicine, None
    

    def get(self, request, pk):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        medicine, response = self.get_medicine(pk, pharmacy)
        if not medicine:
            return response   
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        medicine, response = self.get_medicine(pk, pharmacy)
        if not medicine:
            return response
        
        data = request.data
        serializer = MedicineSerializer(medicine, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        medicine, response = self.get_medicine(pk, pharmacy)
        if not medicine:
            return response
        
        data = request.data
        serializer = MedicineSerializer(medicine, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pharmacy = request.pharmacy
        if not pharmacy:
            return Response(
                {"error": "You must be logged in as a pharmacy to access this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        medicine, response = self.get_medicine(pk, pharmacy)
        if not medicine:
            return response
        
        medicine.delete()
        return Response(
            {"message": "Medicine Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
        
class OwnerPharmacyMedicineListCreateView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsOwnerNotStuff]
    serializer_class = MedicineSerializer
    
    def get_queryset(self):
        pharmacy_id = self.kwargs.get("pharmacy_id")
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        
        if pharmacy.owner != self.request.user.owner:
            raise PermissionDenied("you do not OWN this pharmacy")
        return Medicine.objects.filter(pharmacy=pharmacy)
    
    def perform_create(self, serializer):
        pharmacy_id = self.kwargs.get("pharmacy_id")
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        
        if pharmacy.owner != self.request.user.owner:
            raise PermissionDenied("you do not OWN this pharmacy")
        
        serializer.save(pharmacy=pharmacy)
        
        
class OwnerPharmacyMedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerNotStuff]
    serializer_class = MedicineSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        pharmacy_id = self.kwargs.get("pharmacy_id")
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)

        if pharmacy.owner != self.request.user.owner:
            raise PermissionDenied("You don't own this pharmacy.")
        
        return Medicine.objects.filter(pharmacy=pharmacy)