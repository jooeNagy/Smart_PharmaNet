from django.urls import path
# from .views import UserListView
from .views import OwnerSearchView



urlpatterns = [
    path('', OwnerSearchView.as_view(), name='owner-search'),
]