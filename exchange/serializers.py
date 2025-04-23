from rest_framework import serializers
from medicine.models import *
from .models import *




class ExchangeMedcieneSerializer(serializers.ModelSerializer):
    
    medicine_name = serializers.CharField(source= 'medicine.name', read_only=True)
    medicine_price_to_sell = serializers.CharField(source= 'medicine.price_sell', read_only=True)
    medicine_quantity_to_sell = serializers.CharField(source= 'medicine.quantity_to_sell', read_only=True)
    
    pharmacy_name = serializers.CharField(source= 'medicine.pharmacy.name', read_only=True)
    pharmacy_latitude = serializers.CharField(source= 'medicine.pharmacy.latitude', read_only=True)
    pharmacy_longitude = serializers.CharField(source= 'medicine.pharmacy.longitude', read_only=True)
    
    
    
    
    class Meta:
        model = ExchangeMedciene
        fields = ['medicine_name','medicine_price_to_sell', 'medicine_quantity_to_sell', 'pharmacy_name', 'pharmacy_latitude', 'pharmacy_longitude']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        medicine = data.get("medicine")
        quantity = data.get("quantity")

        if medicine.quantity_to_sell < quantity:  # ✅ Check exchange stock
            raise serializers.ValidationError(
                {"quantity": "Exceeds available exchange quantity."}
            )
        return data



class UpdateMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['can_be_sell', 'quantity_to_sell']