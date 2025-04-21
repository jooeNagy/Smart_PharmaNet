from rest_framework import serializers
from .models import *



class ExchangeMedcieneSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source= 'medicine.name', read_only=True)
    medicine_price = serializers.CharField(source= 'medicine.price', read_only=True)
    medicine_quantity_to_sell = serializers.CharField(source= 'medicine.quantity_to_sell', read_only=True)
    
    
    pharmacy_name = serializers.CharField(source= 'medicine.pharmacy.name', read_only=True)
    pharmacy_location = serializers.CharField(source= 'medicine.pharmacy.location', read_only=True)
    
    
    
    class Meta:
        model = ExchangeMedciene
        fields = ['medicine_name','medicine_price', 'medicine_quantity_to_sell', 'pharmacy_name', 'pharmacy_location']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        medicine = data.get("medicine")
        quantity = data.get("quantity")

        if medicine.quantity < quantity:
            raise serializers.ValidationError({"quantity": "Requested quantity exceeds available stock."})

        return data
    



class UpdateMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['can_be_sell', 'quantity_to_sell']