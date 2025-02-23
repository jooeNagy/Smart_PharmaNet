from django.urls import path
from .views import MedicineListCreateView, MedicineRetrieveUpdateDestroyView



urlpatterns = [
    path('medicine-list/', MedicineListCreateView.as_view()),
    path('new-medicine/<int:pk>', MedicineRetrieveUpdateDestroyView.as_view())
]