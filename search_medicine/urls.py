from django.urls import path
from .views import OwnerSearchView, ImageSearchView



urlpatterns = [
    path('', OwnerSearchView.as_view(), name='owner-search'),
    path('image/', ImageSearchView.as_view(), name='search-with-image'),
]