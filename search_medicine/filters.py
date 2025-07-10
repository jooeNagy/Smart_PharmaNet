from rest_framework import filters
from medicine.models import Medicine
from medicine.serializers import MedicineSerializer
import django_filters
from accounts.models import Pharmacy


class SearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ChoiceFilter(choices=Medicine.CATEGORY_CHOICES)
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_sell_min = django_filters.NumberFilter(field_name='price_sell', lookup_expr='gte')
    price_sell_max = django_filters.NumberFilter(field_name='price_sell', lookup_expr='lte')
    can_be_sell = django_filters.BooleanFilter()
    pharmacy = django_filters.ModelChoiceFilter(queryset=Pharmacy.objects.all())
    exp_date_after = django_filters.DateFilter(field_name='exp_date', lookup_expr='gte')
    
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'price_min', 'price_max', 'price_sell_min', 'price_sell_max', 'can_be_sell', 'pharmacy', 'exp_date_after']