from django.urls import path
from .views import MedicineCreateReadView, MedicineRetrieveUpdateDestroy



urlpatterns = [
    path('medicines/', MedicineCreateReadView.as_view(), name='medicine-list-add'),
    path('medicines/<int:pk>/', MedicineRetrieveUpdateDestroy.as_view(), name='medicine-retrieve-update-destroy'),
]