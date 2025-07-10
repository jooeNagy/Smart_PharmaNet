from functools import cache
from math import e
from rest_framework.response import Response
from medicine.models import Medicine
from rest_framework import generics, filters, status
from medicine.serializers import MedicineSerializer
from django_filters.rest_framework import DjangoFilterBackend
from medicine.models import Medicine
from medicine.serializers import MedicineSerializer
from django.conf import settings
from .filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.db.models import Q
from difflib import get_close_matches
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time


class MedicinePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

@method_decorator(cache_page(60*5), name='dispatch')
class OwnerSearchView(generics.ListAPIView): 
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    filterset_class = SearchFilter
    filter_backends = [DjangoFilterBackend, 
    filters.SearchFilter,
    filters.OrderingFilter]
    
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price','quantity']
    pagination_class = MedicinePagination
    permission_classes = [AllowAny]


    def get_queryset(self):
        # Optimize the query with select_related
        queryset = Medicine.objects.select_related('pharmacy').order_by('id')
        
        # Optional: Add logging to monitor performance
        print(f"Base queryset count: {queryset.count()}")
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        start_time = time.time()
        response = super().list(request, *args, **kwargs)
        end_time = time.time()
        
        print(f"API response time: {end_time - start_time:.2f} seconds")
        return response
    
class ImageSearchView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Image file to upload'
                    }
                }
            }
        },
        responses={
            200: MedicineSerializer(many=True),  
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT
        }
    )
    
    
    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response(
                {"error": "No Image File Provided!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        image_file = request.FILES['image']
        
        try:
            
            if hasattr(image_file, 'seekable') and image_file.seekable():
                image_file.seek(0)
        
            OCR_API_URL = settings.OCR_API_URL
            OCR_API_KEY = settings.OCR_API_KEY
            
            files = {'image': (image_file.name, image_file, image_file.content_type)}
            headers = {'X-API-Key': OCR_API_KEY}
            
            ocr_response = requests.post(
                OCR_API_URL,
                files=files,
                headers=headers,
                timeout=30
            )                                
            ocr_response.raise_for_status()
            ocr_result = ocr_response.json()
            
            extracted_text = ocr_result.get('extracted_text', [])
            cleaned_text = ocr_result.get('cleaned_text', [])
            search_text = cleaned_text if cleaned_text else extracted_text
            if not search_text:
                return Response(
                    {"error": "No text Found in Image"},
                    status=status.HTTP_204_NO_CONTENT
                )
            all_medicine_names = list(Medicine.objects.values_list('name', flat=True))    
            best_match = self.find_medicine_match(search_text, all_medicine_names)    
            
            if not best_match:
                return Response(
                    {
                        "message": "No Matching Medicines found!",
                        "ocr_result": {
                            "extracted_text": extracted_text,
                            "cleaned_text": cleaned_text,
                            "processing_time": ocr_result.get('processing_time', {})
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
                
            matching_medicines = Medicine.objects.filter(
                Q(name__in=best_match)|
                Q(name__iregex=r'(' + '|'.join(best_match) + ')')
            ).distinct()
            
            serializer = MedicineSerializer(matching_medicines, many=True)
            
            return Response({
                'ocr_result': {
                    'extracted_text': extracted_text,
                    'cleaned_text': cleaned_text,
                    'processing_time': ocr_result.get('processing_time', {})
                },
                'search_result': serializer.data,
                'count': matching_medicines.count(),
                'matched_terms': best_match
            })
                
        except requests.RequestException as e:
            return Response(
                {"error": f"error connecting to OCR model: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"an error occured: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
    def find_medicine_match(self, ocr_text, medicine_names):
        matches = set()
        medicine_names_lower = [name.lower() for name in medicine_names]
        combined_text = ' '.join(ocr_text).lower()
        words = combined_text.split()
        for word in words:
            if len(word) > 3:
                close_matches = get_close_matches(word, medicine_names_lower, n=3, cutoff=0.6)
                for match in close_matches:
                    original_name = medicine_names[medicine_names_lower.index(match)]
                    matches.add(original_name)
        return list(matches) if matches else None