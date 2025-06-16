from django.db import models
from rest_framework import serializers
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
    can_be_sell = models.BooleanField(null=False, blank=True, default=False)
    quantity_to_sell = models.IntegerField(null=True, blank=True)  # Fixed: Added blank=True
    price_sell = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)
    
    # Buy = models.BooleanField(null=True, default=False)
    # quantity_to_Buy = models.IntegerField(null=True, blank=False)  # Fixed: Added blank=True
    
    
    def __str__(self):
        return self.name
    
    def clean(self):
    # Validate expiration date
        if self.exp_date <= date.today():
            raise ValidationError({"exp_date": "Expiration Date cannot be in the past"})
        
        if self.can_be_sell:
            # Validate when can_be_sell=True
            if self.quantity_to_sell is None:
                raise ValidationError({"quantity_to_sell": "Required when can_be_sell=True."})
            if self.quantity_to_sell > self.quantity:
                raise ValidationError({
                    "quantity_to_sell": f"Quantity to sell ({self.quantity_to_sell}) cannot exceed available quantity ({self.quantity})"
                })
        else:
            # Clear quantity_to_sell when can_be_sell=False
            self.quantity_to_sell = None  # Explicitly set to None (allowed with blank=True)

    def save(self, *args, **kwargs):
        from exchange.models import ExchangeMedciene, Order_exchange  # Import here to avoid circular import

        self.full_clean()  # Validate fields
        super().save(*args, **kwargs)  # Save FIRST to ensure ID exists

        # Delete exchange entries if can_be_sell=False
        if not self.can_be_sell:
            ExchangeMedciene.objects.filter(
                medicine=self,
                operation=ExchangeMedciene.Status.SELL
            ).delete()
        else:
            # Create/update entry only if can_be_sell=True
            if self.quantity_to_sell and self.quantity_to_sell <= self.quantity:
                ExchangeMedciene.objects.update_or_create(
                    medicine=self,
                    operation=ExchangeMedciene.Status.SELL,
                    defaults={'quantity': self.quantity_to_sell}
                )
            else:
                raise serializers.ValidationError({
                    "quantity_to_sell": "Cannot exceed available quantity"
                })
            
        
        # if not self.Buy:
        #     ExchangeMedciene.objects.filter(
        #         medicine=self,
        #         operation=ExchangeMedciene.Status.BUY
        #     ).delete()
        # else:
        #     if self.quantity_to_Buy <= self.quantity_to_sell:
        #         self.quantity -= self.quantity_to_Buy
        #         self.quantity_to_sell -= self.quantity_to_Buy
        #         self.save()
        #         Order_exchange.objects.update_or_create(
        #             medicine=self,
        #             # pharmacy_buyer='',
        #             defaults={
        #                 'quantity': self.quantity_to_Buy,
        #                 'status': 'Pending',
        #             }
        #         )
        #     else:
        #         raise serializers.ValidationError({
        #             "quantity_to_buy": "Cannot exceed available quantity to sell"
        #         })
            


     