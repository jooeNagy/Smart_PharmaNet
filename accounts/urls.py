from django.urls import path
from .views import OwnerRegisterView, PharmacyCreateView, EmailTokenObtainPairView, LoginPharmacyView, PharmacyRetrieveUpdateDestroy, CustomLogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView


urlpatterns = [
    path('register/', OwnerRegisterView.as_view(), name='owner-registeration'),
    path('pharmacy/', PharmacyCreateView.as_view(), name='pharmacy-create'),                # pharmacies/ --> pharmacy/
    path('pharmacy/<int:pk>/', PharmacyRetrieveUpdateDestroy.as_view(), name='delete-ypdate-pharmacy'),
    path('owner/login/', EmailTokenObtainPairView.as_view(), name='token-obtain-pair'),     # token/      --> owner/login/
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('pharmacy/login/', LoginPharmacyView.as_view(), name='pharmacy-login'),
    path('logout/', CustomLogoutView.as_view(), name='pharmacy-logout'),
    # path('search/', OwnerSearchView.as_view(), name='owner-search'),
]