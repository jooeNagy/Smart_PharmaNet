from django.urls import path
from .views import *



urlpatterns = [
        path('exchange_list/', ExchangeMedicineView.as_view()),
        path('get/pharmcy_seller/orders', Get_BuyOrderMedicineView.as_view()),
        path('buy/order', create_BuyOrderMedicineView.as_view()),
        
        path('update_status/<int:pk>', Notification_updatestatusView.as_view()),
        path('get_notification/', Notification_View.as_view()),
        
        
        path('subscripe/', SubscriptionView.as_view()),    
            
        path('user_purchase/', UserPurchaseView.as_view()), 
]