from django.db import models
from accounts.models import Pharmacy

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=1)
    description = models.TextField(max_length=500)
    price = models.Aggregate
    quantity = models.IntegerField()
    exp_date = models.DateField()
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)


    def __str__(self):
        return self.name