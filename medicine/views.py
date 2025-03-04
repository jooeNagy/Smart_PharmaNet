from django.shortcuts import render
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Owner, Pharmacy


class OwnerPharmacyMixin:
    def get_owner_and_pharmacy(self, user):
            try:
                owner = Owner.objects.get(user=user)
            except Owner.DoesNotExist:
                return Response(
                    {"error": "No Owner Found for the logged-in User"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pharmacies = owner.pharmacies.all()
            if not pharmacies:
                return Response(
                    {"error": "No Pharmacies found for the logged-in user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return owner, pharmacies.first()



class MedicineCreateReadView(OwnerPharmacyMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        
        medicines = Medicine.objects.filter(pharmacy__in=owner.pharmacies.all())
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
        
    def post(self,request):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        
        data = request.data
        data['pharmacy'] = response.id

        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineRetrieveUpdateDestroy(OwnerPharmacyMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get_medicine(self, pk, owner):
        try:
            medicine = Medicine.objects.get(id=pk)
        except Medicine.DoesNotExist:
            return None, Response(
                {"error": "Medicine not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if medicine.pharmacy not in owner.pharmacies.all():
            return None, Response(
                {"error": "You do not have permission to access this medicine"},
                status=status.HTTP_403_FORBIDDEN
            )
        return medicine, None
    

    def get(self, request, pk):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        medicine, response = self.get_medicine(pk, owner)
        if not medicine:
            return response
        
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        medicine, response = self.get_medicine(pk, owner)
        if not medicine:
            return response
        
        data = request.data
        serializer = MedicineSerializer(medicine, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        medicine, response = self.get_medicine(pk, owner)
        if not medicine:
            return response
        
        data = request.data
        serializer = MedicineSerializer(medicine, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = request.user
        owner, response = self.get_owner_and_pharmacy(user)
        if not owner:
            return response
        medicine, response = self.get_medicine(pk, owner)
        if not medicine:
            return response
        
        medicine.delete()
        return Response(
            {"message": "Medicine Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )