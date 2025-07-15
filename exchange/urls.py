from django.urls import path
from .views import *



urlpatterns = [
        path('exchange_list/', ExchangeMedicineView.as_view()),
        
        path('get/pharmcy_seller/orders/', Get_BuyOrderMedicineView.as_view()),
        path('get/pharmcy_seller/orders/<int:pharmacy_id>/', Get_BuyOrderMedicineView.as_view(), name="seller-owner"),
        
        path('buy/order/', create_BuyOrderMedicineView.as_view()),  
        path('buy/order/pharmacy/<int:pharmacy_id>/', create_BuyOrderMedicineView.as_view()),
              
        path('update_status/<int:pk>/', Notification_updatestatusView.as_view()),
        
        path('get_notification/', Notification_View.as_view()), 
        path('get_notification/pharmacy/<int:pharmacy_id>/', Notification_View.as_view()),    
        
        path('get_orders_request/', MyOrderRequestView.as_view()), 
        path('get_orders_request/pharmacy/<int:pharmacy_id>/', MyOrderRequestView.as_view()),  
           
        path('subscripe/', SubscriptionView.as_view()),           
        path('subscripe/pharmacy/<int:pharmacy_id>/', SubscriptionView.as_view()), 
        
        path('user_purchase/', UserPurchaseView.as_view()), 
]