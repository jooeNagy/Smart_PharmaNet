from rest_framework import serializers
from .models import Medicine
from datetime import date
from drf_spectacular.utils import extend_schema_field
import requests
from django.conf import settings


class MedicineSerializer(serializers.ModelSerializer):
    pharmacy_location = serializers.SerializerMethodField()
    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ['pharmacy_location']
        
        
    @extend_schema_field(serializers.CharField)
    def get_pharmacy_location(self, obj):
        if not obj.pharmacy:
            return None
        return {
            'latitude': float(obj.pharmacy.latitude) if obj.pharmacy.latitude else None,
            'longitude': float(obj.pharmacy.longitude) if obj.pharmacy.longitude else None,
            'pharmacy_name': obj.pharmacy.name,
            'city': obj.pharmacy.city
        }        

    def validate_exp_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Expiration Date must be a Future Date")
        return value
    
    def validate(self, data):
        if data.get('can_be_sell') and data.get('quantity_to_sell') is None:
            raise serializers.ValidationError({
                "quantity_to_sell": "This field is required when can_be_sell is True"
            })

        if data.get('quantity_to_sell') is not None and data.get('quantity') is not None:
            if data['quantity_to_sell'] > data['quantity']:
                raise serializers.ValidationError({
                    "quantity_to_sell": "Cannot exceed available quantity"
                })

        if data.get('quantity_to_buy') is not None and data.get('quantity_to_sell') is not None:
            if data['quantity_to_buy'] > data['quantity_to_sell']:
                raise serializers.ValidationError({
                    "quantity_to_buy": "Cannot exceed available quantity to sell"
                }) 
        return data


