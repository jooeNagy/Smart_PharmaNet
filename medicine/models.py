from django.db import models
from accounts.models import Pharmacy
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError 

User = get_user_model()

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Dental and oral agents', "Dental and oral agents"),
        ('Blood products', "Blood products"),
        ('Antibiotics', "Antibiotics"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)
    quantity = models.PositiveIntegerField()
    exp_date = models.DateField()
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
    def clean_data(self):
        if self.exp_date <= date.today():
            raise ValidationError({"exp_date": "Expiration Date cannot be in the past"})