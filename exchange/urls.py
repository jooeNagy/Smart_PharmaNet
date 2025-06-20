from django.urls import path
from .views import ExchangeMedicineView,Get_BuyOrderMedicineView ,create_BuyOrderMedicineView, Notification_updatestatusView



urlpatterns = [
        path('exchange_list/', ExchangeMedicineView.as_view()),
        path('get/pharmcy_seller/orders', Get_BuyOrderMedicineView.as_view()),
        path('buy/order', create_BuyOrderMedicineView.as_view()),
        
        path('update_status/<int:pk>', Notification_updatestatusView.as_view()),
        
        
]