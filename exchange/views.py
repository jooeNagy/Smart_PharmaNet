from django.shortcuts import render, get_object_or_404  
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404  
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import ExchangeMedciene, Buy_Order
from .serializers import (
    ExchangeMedcieneSerializer,
    Create_BuyOrderMedcieneSerializer,
    Get_orders_toseller_OrderMedcieneSerializer,
    BuyOrder_update_status_Serializer
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
        if not self.request.pharmacy:
            raise PermissionDenied("Authenticated pharmacy not found.")
        if order.pharmacy_seller != self.request.pharmacy:
            raise PermissionDenied("You can only update orders for your own pharmacy.")
        return order
