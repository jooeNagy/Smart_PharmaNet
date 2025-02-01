from django.contrib import admin
# from mapwidgets.widgets import GooglePointFieldWidget
from .models import Owner, Pharmacy

# Register your models here.


# class PharmacyAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         PharmacyProfile.PointField: {'widget': GooglePointFieldWidget}
    # }
admin.site.register(Pharmacy)
admin.site.register(Owner)