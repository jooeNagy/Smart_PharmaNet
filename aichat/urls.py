from django.urls import path
from . import views

urlpatterns = [
    path('ai/', views.ChatAPIView.as_view(), name="aichat")
]