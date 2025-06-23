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
class Create_BuyOrderMedcieneSerializer(serializers.ModelSerializer):
    
    medicine_name = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Medicine.objects.all()
    )
    
    pharmacy_seller = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Pharmacy.objects.all()
    )
    pharmacy_buyer = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Pharmacy.objects.all()
    )
    class Meta:
        model = Buy_Order
        fields = ['medicine_name','price','pharmacy_seller','pharmacy_buyer', 'quantity', 'status', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        medicine = data.get("medicine_name")
        quantity = data.get("quantity")

        if medicine and hasattr(medicine, 'quantity_to_sell'):
            if quantity > medicine.quantity_to_sell:
                raise serializers.ValidationError(
                    {"quantity": "Exceeds available exchange quantity."}
                )
        return data

class Get_orders_toseller_OrderMedcieneSerializer(serializers.ModelSerializer):
    med_name = serializers.CharField(source='medicine_name.name', read_only=True)
    pharma_buyer = serializers.CharField(source='pharmacy_buyer.name', read_only=True)
    class Meta:
        model = Buy_Order
        fields = ['id', 'med_name','price', 'quantity', 'pharma_buyer',  'status', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        medicine = data.get("medicine_name")
        quantity = data.get("quantity")

        if medicine and hasattr(medicine, 'quantity_to_sell'):
            if quantity > medicine.quantity_to_sell:
                raise serializers.ValidationError(
                    {"quantity": "Exceeds available exchange quantity."}
                )
        return data
    
class BuyOrder_update_status_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Buy_Order
        fields = ['status']
        

class UpdateMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['can_be_sell', 'quantity_to_sell']
        
        
class NotificatoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        

class SubscriptionSerializer(serializers.ModelSerializer):
    
    pharmacy = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Pharmacy.objects.all()
    )
    class Meta:
        model = Subscription
        fields = ['pharmacy', 'type', 'created_at']
            
    