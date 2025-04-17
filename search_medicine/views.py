from django.shortcuts import render
from medicine.models import Medicine
from rest_framework import generics, filters, status
from medicine.serializers import MedicineSerializer
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SearchFilter
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser



class OwnerSearchView(generics.ListAPIView): 
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()  
    filterset_class = SearchFilter
    filter_backends = [DjangoFilterBackend, 
    filters.SearchFilter,
    filters.OrderingFilter]
    
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price','quantity']
