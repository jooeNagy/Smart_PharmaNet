from django.urls import path
from .views import OwnerRegisterView, PharmacyCreateView, EmailTokenObtainPairView, CustomLogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView


urlpatterns = [
    path('register/', OwnerRegisterView.as_view(), name='owner-registeration'),
    path('pharmacies/', PharmacyCreateView.as_view(), name='pharmacy-create'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', CustomLogoutView.as_view(), name='token-blacklist'),
]