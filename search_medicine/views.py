from django.shortcuts import render
from medicine.models import Medicine
from rest_framework import generics, filters, status
from medicine.serializers import MedicineSerializer
# from rest_framework_word_filter import FullWordSearchFilter
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SearchFilter
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
from django.db.models import Q



class OwnerSearchView(generics.ListAPIView): 
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()  
    filterset_class = SearchFilter
    filter_backends = [DjangoFilterBackend, 
    filters.SearchFilter,
    filters.OrderingFilter]
    
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price','quantity']

    
class MedicineImageSearchView(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = MedicineSerializer
    
    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        # 1 - read the uploaded image
        uploaded_image = request.FILES['image']
        image_data = uploaded_image.read()
        # 2 - convert to opencv format
        pil_image = Image.open(io.BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        # 3 - extract text using OCR
        extracted_text = self.extract_text_from_image(cv_image)
        # 4 - search for medicine in DB
        medicines = self.search_medicine_by_text(extracted_text)
        serializer = MedicineSerializer(medicines, many=True)
        return Response({
            'extracted_text': extracted_text,
            'result': serializer.data
        })
        
    def extract_text_from_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(thresh)
        return text.lower().strip()
    
    def search_medicine_by_text(self, text):
        if not text:
            return Medicine.objects.none()
        words = [word for word in text.split() if len(word) > 3]
        if not words:
            return Medicine.objects.none()
        query = Q()
        for word in words:
            query |= Q(name__icontains=word) | Q(generic_name__icontains=word)
        return Medicine.objects.filter(query).distinct()