from django.shortcuts import render
from .models import Owner, Pharmacy
from .serializers import OwnerSerializer, PharmacySerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# Create your views here.


class OwnerRegisterView(generics.CreateAPIView):
    serializer_class = OwnerSerializer


class PharmacyCreateView(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        try:
            owner = user.owner
        except Owner.DoesNotExist:
            return Response(
                {"detail": "User has no associated profile"},
                status = status.HTTP_400_BAD_REQUEST
            ) 
        serializer.save(owner=owner)