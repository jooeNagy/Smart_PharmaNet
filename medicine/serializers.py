from rest_framework import serializers
from .models import Medicine
from datetime import date

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'category', 'description', 'price', 'quantity', 'exp_date', 'pharmacy']

    def validate_exp_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Expiration Date must be a Future Date")
        return value