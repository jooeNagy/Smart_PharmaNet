from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
# Create your models

class Owner(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=11, null=True)
    nationalID = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    

    def __str__(self):
        return self.user.username
    

class Pharmacy(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pharmacies')
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    license_number = models.CharField(max_length=50)
    password = models.CharField(max_length=128, null=True, blank=True)
    number_sells = models.IntegerField(default=0)
    number_buys = models.IntegerField(default=0)
    

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name
    
    
    
