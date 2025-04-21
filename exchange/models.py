from django.db import models
from medicine.models import *
# Create your models here.

class ExchangeMedciene(models.Model):
    class Status(models.TextChoices):
        SELL = 'Sell'
        BUY = 'Buy'

    operation = models.CharField(max_length=5, choices=Status.choices, blank=False)   
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="exchanges")  # ✅ Added `related_name`
    quantity = models.IntegerField(null=False, blank=False, default=1)  
    
    def __str__(self):
        return f"{self.medicine.name} - {self.operation} ({self.quantity})"