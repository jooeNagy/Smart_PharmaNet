from rest_framework import serializers
from .models import Medicine
from datetime import date
from drf_spectacular.utils import extend_schema_field
import requests
from django.conf import settings


def get_google_image(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": settings.GOOGLE_CSE_API_KEY,
        "cx": settings.GOOGLE_CSE_ID,
        "q": query,
        "searchType": "image",
        "num": 1  # Only need 1 image
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]  # image URL
    except Exception as e:
        print("Google CSE image error:", str(e))

    return "https://via.placeholder.com/400x300?text=No+Image"

class MedicineSerializer(serializers.ModelSerializer):
    pharmacy_location = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ['pharmacy_location']
        
    def get_image_url(self, obj):
        return get_google_image(obj.name)
        
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


