from django.urls import path
from .views import ExchangeMedicineView,Get_BuyOrderMedicineView , Notification_View,create_BuyOrderMedicineView, Notification_updatestatusView, SubscriptionView



urlpatterns = [
        path('exchange_list/', ExchangeMedicineView.as_view()),
        path('get/pharmcy_seller/orders', Get_BuyOrderMedicineView.as_view()),
        path('buy/order', create_BuyOrderMedicineView.as_view()),
        
        path('update_status/<int:pk>', Notification_updatestatusView.as_view()),
        path('get_notification/', Notification_View.as_view()),
        
        
        path('subscribe/', SubscriptionView.as_view()),       
]