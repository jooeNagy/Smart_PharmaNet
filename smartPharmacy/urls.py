from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

# for documing api
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('medicine/', include('medicine.urls')),
    path('account/', include('accounts.urls')),
    path('search_medicine/', include('search_medicine.urls')),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
    # for documing api
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
