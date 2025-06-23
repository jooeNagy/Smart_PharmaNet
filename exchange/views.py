from django.shortcuts import render, get_object_or_404  
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404  
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import ExchangeMedciene, Buy_Order, Notification, Subscription
from .serializers import (
    ExchangeMedcieneSerializer,
    Create_BuyOrderMedcieneSerializer,
    Get_orders_toseller_OrderMedcieneSerializer,
    BuyOrder_update_status_Serializer,
    NotificatoinSerializer,
    SubscriptionSerializer
)

from medicine.models import Medicine
from medicine.serializers import MedicineSerializer

from accounts.authentication import PharmacyJWTAuthentication


# 🔄 Update / Delete Medicine
class MedicineRetrieveUpdateDestroyView(generics.UpdateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


# 🔁 List All Exchange Requests
class ExchangeMedicineView(generics.ListAPIView):
    queryset = ExchangeMedciene.objects.all()
    serializer_class = ExchangeMedcieneSerializer
    permission_classes = [IsAuthenticated]


# 📦 Get All Orders Made to the Authenticated Pharmacy Seller
class Get_BuyOrderMedicineView(generics.ListAPIView):  
    serializer_class = Get_orders_toseller_OrderMedcieneSerializer  
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_queryset(self):
        pharmacy = getattr(self.request, "pharmacy", None)

        if not pharmacy:
            raise PermissionDenied("You must be authenticated as a pharmacy to view orders.")
        elif Buy_Order.objects.filter(pharmacy_seller=pharmacy).count() == 0:
            raise PermissionDenied("No orders found for this pharmacy.")
        return Buy_Order.objects.filter(pharmacy_seller=pharmacy)

        

# 📝 Create a New Buy Order
class create_BuyOrderMedicineView(generics.CreateAPIView):
    serializer_class = Create_BuyOrderMedcieneSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]


# 🔔 Update Buy Order Status
class Notification_updatestatusView(generics.RetrieveUpdateAPIView):
    queryset = Buy_Order.objects.all()
    serializer_class = BuyOrder_update_status_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_object(self):
        order = super().get_object()
        pharmacy = getattr(self.request, "pharmacy", None)
        if not pharmacy:
            raise PermissionDenied("Authenticated pharmacy not found.")
        if order.pharmacy_seller != pharmacy:
            raise PermissionDenied("You can only update orders for your own pharmacy.")
        return order
    
    
    def perform_update(self, serializer):
        # Capture current status before update
        old_status = self.get_object().status
        # Save the updated order
        order = serializer.save()
        # Create notification for buyer if status changed
        if old_status != 'Pending':
            self.create_notification(order, old_status)

    def create_notification(self, order, old_status):
        """Create notification for buyer when status changes"""
        message = (
            f"Your Order #{order.medicine_name.name} from {order.pharmacy_seller.name} pharmacy status changed: "
            f"{old_status} → {order.status}"
        )
        
        notification = Notification.objects.create(
            pharmacy=order.pharmacy_buyer,  # Set pharmacy to buyer
            order=order,
            message=message
        )
        
        # print(f"Notification created: ID {notification.id}")
        return notification
    
    
class Notification_View(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificatoinSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_queryset(self):
        pharma_req = getattr(self.request, "pharmacy", None)

        if not pharma_req:
            raise PermissionDenied("You must be authenticated as a pharmacy to view orders.")
        
        if Notification.objects.filter(pharmacy=pharma_req).count() == 0:
            raise PermissionDenied("No Notifications found for this pharmacy.")
        
        return Notification.objects.filter(pharmacy=pharma_req)

  
class SubscriptionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [PharmacyJWTAuthentication]

    