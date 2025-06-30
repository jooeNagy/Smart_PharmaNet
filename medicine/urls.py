from django.urls import path
from .views import MedicineCreateReadView, MedicineRetrieveUpdateDestroy, OwnerPharmacyMedicineListCreateView, OwnerPharmacyMedicineDetailView



urlpatterns = [
    path('medicines/', MedicineCreateReadView.as_view(), name='medicine-list-add'),
    path('medicines/<int:pk>/', MedicineRetrieveUpdateDestroy.as_view(), name='medicine-retrieve-update-destroy'),
    path('owner/pharmacies/<int:pharmacy_id>/medicines/', OwnerPharmacyMedicineListCreateView.as_view(), name="owner-pharmacy-medicines"),
    path("owner/pharmacies/<int:pharmacy_id>/medicines/<int:pk>/", OwnerPharmacyMedicineDetailView.as_view(), name="update-delete-modeicine"),
]