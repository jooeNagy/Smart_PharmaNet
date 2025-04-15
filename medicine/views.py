from django.shortcuts import render
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Owner, Pharmacy

class MedicineCreateReadView(APIView):
    permission_classes = [IsAuthenticated]

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