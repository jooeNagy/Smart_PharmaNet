from django.urls import path
from .views import OwnerRegisterView, PharmacyCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# for documing api
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('register/', OwnerRegisterView.as_view(), name='owner-registeration'),
    path('pharmacies/', PharmacyCreateView.as_view(), name='pharmacy-create'),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    
    # for documing api
     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]