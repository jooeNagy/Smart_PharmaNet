from django.contrib import admin

from .models import Owner, Pharmacy

# Register your models here.

admin.site.register(Pharmacy)
admin.site.register(Owner)