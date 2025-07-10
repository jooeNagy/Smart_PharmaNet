from django.db import models
from rest_framework import serializers
from accounts.models import Pharmacy
from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError
import urllib.parse
from .utils import fetch_google_image_url 

User = get_user_model()

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Dental and oral agents', "Dental and oral agents"),
        ('Blood products', "Blood products"),
        ('Antibiotics', "Antibiotics"),
        ('Analgesics', "Analgesics"),
        ('Anti-inflammatory drugs', "Anti-inflammatory drugs"),
        ('Cardiovascular medications', "Cardiovascular medications"),
        ('Antidiabetic drugs', "Antidiabetic drugs"),
        ('Antihistamines', "Antihistamines"),
        ('Antacids and digestive aids', "Antacids and digestive aids"),
        ('Respiratory medications', "Respiratory medications"),
        ('Antifungal medications', "Antifungal medications"),
        ('Antiviral medications', "Antiviral medications"),
        ('Hormones and hormone modulators', "Hormones and hormone modulators"),
        ('Vaccines and immunizations', "Vaccines and immunizations"),
        ('Dermatological preparations', "Dermatological preparations"),
        ('Ophthalmic preparations', "Ophthalmic preparations"),
        ('Ear, nose, and throat preparations', "Ear, nose, and throat preparations"),
        ('Vitamins and minerals', "Vitamins and minerals"),
        ('Antidepressants', "Antidepressants"),
        ('Anxiolytics and sedatives', "Anxiolytics and sedatives"),
        ('Anticonvulsants', "Anticonvulsants"),
        ('Muscle relaxants', "Muscle relaxants"),
        ('Diuretics', "Diuretics"),
        ('Laxatives', "Laxatives"),
        ('Contraceptives', "Contraceptives"),
        ('Oncology medications', "Oncology medications"),
        ('Immunosuppressants', "Immunosuppressants"),
        ('Anesthetics', "Anesthetics"),
        ('Emergency medications', "Emergency medications"),
        ('Herbal and alternative medicines', "Herbal and alternative medicines"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)
    quantity = models.PositiveIntegerField()
    exp_date = models.DateField()
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    can_be_sell = models.BooleanField(null=False, blank=True, default=False)
    quantity_to_sell = models.IntegerField(null=True, blank=True)
    price_sell = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0.00)
    image_url = models.URLField(null=True, blank=True)
    
    
    
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
        from exchange.models import ExchangeMedciene  # Import here to avoid circular import

        self.full_clean()  # Validate fields
        
        is_new = self._state.adding
        old_name = None
        if not is_new:
            try:
                old_instance = Medicine.objects.get(pk=self.pk)
                old_name = old_instance.name
            except Medicine.DoesNotExist:
                pass
        
        if is_new or (old_name and old_name != self.name):
            self.image_url = fetch_google_image_url(self.name)
            
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