from rest_framework import serializers
from .models import Medicine
from datetime import date

class MedicineSerializer(serializers.ModelSerializer):
    pharmacy_location = serializers.SerializerMethodField()
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'category', 'description', 'price', 'quantity', 'exp_date', 'pharmacy', 'pharmacy_location']
        read_only_fields = ['pharmacy_location']
        
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