from django.urls import path
from .views import ExchangeMedicineView



urlpatterns = [
        path('exchange_list/', ExchangeMedicineView.as_view()),
]