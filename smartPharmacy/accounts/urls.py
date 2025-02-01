from django.urls import path
from .views import OwnerRegisterView, PharmacyCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', OwnerRegisterView.as_view(), name='owner-registeration'),
    path('pharmacies/', PharmacyCreateView.as_view(), name='pharmacy-create'),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]