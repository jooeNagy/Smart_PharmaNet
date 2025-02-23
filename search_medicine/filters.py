from rest_framework import filters
from medicine.models import Medicine
from medicine.serializers import MedicineSerializer
import django_filters


class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Medicine
        fields = {
            'name': ['iexact', 'icontains'],     
        }