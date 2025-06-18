from django.shortcuts import render
from .models import ExchangeMedciene, Buy_Order
from medicine.models import *
from medicine.serializers import MedicineSerializer

from .serializers import ExchangeMedcieneSerializer, BuyOrderMedcieneSerializer,BuyOrder_update_status_Serializer
# from  ExchangeMedcieneSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404  # ✅ Import added
from rest_framework.response import Response


class MedicineRetrieveUpdateDestroyView(generics.UpdateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

from accounts.authentication import PharmacyJWTAuthentication
class ExchangeMedicineView(generics.ListAPIView):
    queryset = ExchangeMedciene.objects.all()
    serializer_class = ExchangeMedcieneSerializer
    permission_classes = [IsAuthenticated]


class Get_BuyOrderMedicineView(generics.ListAPIView):  
    serializer_class = BuyOrderMedcieneSerializer  
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_queryset(self):
        return Buy_Order.objects.filter(pharmacy_seller=self.request.user)

class create_BuyOrderMedicineView(generics.CreateAPIView):
    queryset = Buy_Order.objects.all()
    serializer_class = BuyOrderMedcieneSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]
    

class Notification_updatestatusView(generics.UpdateAPIView):
    queryset = Buy_Order.objects.all()
    serializer_class = BuyOrder_update_status_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_object(self):
        order = super().get_object()
        # Verify the current user is the pharmacy seller
        if order.pharmacy_seller != self.request.user:
            raise PermissionDenied("You can only update orders for your own pharmacy")
        return order