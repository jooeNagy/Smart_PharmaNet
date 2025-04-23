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
    can_be_sell = models.BooleanField(null=False, blank=False, default=False)
    quantity_to_sell = models.IntegerField(null=True)
    price_sell = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)

    def __str__(self):
        return self.name
    
    def clean(self):
        # Existing validations
        if self.exp_date <= date.today():
            raise ValidationError({"exp_date": "Expiration Date cannot be in the past"})
        if self.can_be_sell and self.quantity_to_sell is None:
            raise ValidationError({"quantity_to_sell": "Required when can_be_sell=True."})
        
        # New validation: quantity_to_sell must be <= quantity
        if self.quantity_to_sell and self.quantity_to_sell > self.quantity:
            raise ValidationError({
                "quantity_to_sell": f"Quantity to sell ({self.quantity_to_sell}) cannot exceed available quantity ({self.quantity})"
            })

    def save(self, *args, **kwargs):
        from exchange.models import ExchangeMedciene
        
        self.full_clean()  # This will enforce all validations
        created = not self.pk
        super().save(*args, **kwargs)
        
        if created and self.can_be_sell and self.quantity_to_sell and (self.quantity - self.quantity_to_sell >= 0):
            ExchangeMedciene.objects.create(
                medicine=self,
                operation=ExchangeMedciene.Status.SELL,
                quantity=self.quantity_to_sell
            )

     