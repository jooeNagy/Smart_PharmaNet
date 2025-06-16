from django.db import models
from medicine.models import Medicine, Pharmacy  # Import necessary models
class ExchangeMedciene(models.Model):
    class Status(models.TextChoices):
        SELL = 'Sell'
        BUY = 'Buy'

    operation = models.CharField(max_length=5, choices=Status.choices, blank=False)
    medicine = models.ForeignKey(
        'medicine.Medicine',  # String reference to avoid circular import
        on_delete=models.CASCADE,
        related_name='exchange_entries'  # Valid reverse relation name
    )
    quantity = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.medicine.name} - {self.operation} ({self.quantity})"
    
    
# class Buy_Order(models.Model):
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=False, blank=False, default=1)
#     # pharmacy_buyer = models.ForeignKey('accounts.Pharmacy', on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.medicine.name} ({self.quantity})"
    
        
class Buy_Order(models.Model):
    
    class Status(models.TextChoices):
        Pending = 'Pending'
        Accepted = 'Accepted'
        Rejected = 'Rejected'
    
    medicine_name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)
    pharmacy_seller = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=False, blank=False)
    status = models.CharField(max_length=20, default='Pending', choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Order {self.id} - {self.medicine_name} ({self.quantity})"