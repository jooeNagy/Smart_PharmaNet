from django.urls import path
# from .views import UserListView
from .views import OwnerSearchView, MedicineImageSearchView



urlpatterns = [
    path('', OwnerSearchView.as_view(), name='owner-search'),
    path('image/', MedicineImageSearchView.as_view(), name='image-search')
]