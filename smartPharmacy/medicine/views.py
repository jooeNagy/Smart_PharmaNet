from django.shortcuts import render
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework import generics
# Create your views here.



class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer