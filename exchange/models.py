from django.db import models
from medicine.models import Medicine, Pharmacy  



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
    
        
class Buy_Order(models.Model):   
    class Choices(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'
        CANCELLED = 'Cancelled'
    
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pharmacy_seller = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="orders_sold")
    pharmacy_buyer = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="orders_bought", null=True, blank=True)
    status = models.CharField(max_length=50, choices=Choices.choices, default=Choices.PENDING, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Notification(models.Model):       
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)  # Your current approach
    order = models.ForeignKey(Buy_Order, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Subscription(models.Model):   
    class Choices(models.TextChoices):
        FREE = 'Free'
        PRO = 'Pro'
        MAX = 'Max'
        
    
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=Choices.choices, default=Choices.FREE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)



class UserPurchase(models.Model):   
    username = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)

