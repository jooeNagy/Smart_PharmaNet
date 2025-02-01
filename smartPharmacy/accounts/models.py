from django.db import models
from django.contrib.auth.models import User
# from mapwidgets.widgets import GoogleMapPointFieldWidget

# Create your models

class Owner(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    # name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=11, null=True)
    nationalID = models.CharField(max_length=14)

    def __str__(self):
        return self.user.username
    

class Pharmacy(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pharmacies')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name