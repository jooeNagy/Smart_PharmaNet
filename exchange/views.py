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
    SubscriptionSerializer,
    UserPurchaseSerializer
)
from medicine.models import Medicine
from medicine.serializers import MedicineSerializer
from accounts.authentication import PharmacyJWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Pharmacy



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
        user = self.request.user
        pharmacy = getattr(self.request, "pharmacy", None)
        pharmacy_id = self.kwargs.get("pharmacy_id")

        if pharmacy:
            return Buy_Order.objects.filter(pharmacy_seller=pharmacy)

        elif hasattr(user, 'owner'):
            if pharmacy_id:
                try:
                    pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner=user.owner)
                except Pharmacy.DoesNotExist:
                    raise PermissionDenied("Pharmacy not found or not owned by you.")
                return Buy_Order.objects.filter(pharmacy_seller=pharmacy)

            return Buy_Order.objects.filter(pharmacy_seller__owner=user.owner)

        raise PermissionDenied("Only authenticated pharmacy staff or owners are allowed.")

        

# 📝 Create a New Buy Order
class create_BuyOrderMedicineView(generics.CreateAPIView):
    serializer_class = Create_BuyOrderMedcieneSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        pharmacy = getattr(self.request, "pharmacy", None)
        pharmacy_id = self.kwargs.get("pharmacy_id")

        # Staff: pharmacy is attached from token
        if pharmacy:
            serializer.save(pharmacy_buyer=pharmacy)

        # Owner: pharmacy_id must be passed in URL
        elif hasattr(user, 'owner'):
            if not pharmacy_id:
                raise PermissionDenied("Owner must specify pharmacy_id in URL.")
            try:
                pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner=user.owner)
            except Pharmacy.DoesNotExist:
                raise PermissionDenied("Pharmacy not found or not owned by you.")
            serializer.save(pharmacy_buyer=pharmacy)

        else:
            raise PermissionDenied("Only authenticated pharmacy staff or owners are allowed.")


# 🔔 Update Buy Order Status
class Notification_updatestatusView(generics.RetrieveUpdateAPIView):
    queryset = Buy_Order.objects.all()
    serializer_class = BuyOrder_update_status_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_object(self):
        order = super().get_object()
        pharmacy = getattr(self.request, "pharmacy", None)
        user = self.request.user

        if pharmacy:
            # Logged in as pharmacy staff
            if order.pharmacy_seller != pharmacy:
                raise PermissionDenied("You can only update orders for your own pharmacy.")
        elif hasattr(user, "owner"):
            # Logged in as owner
            if order.pharmacy_seller.owner != user.owner:
                raise PermissionDenied("You don't own this pharmacy.")
        else:
            raise PermissionDenied("Only pharmacy staff or owners are allowed.")
        
        return order
       
    def perform_update(self, serializer):
        # Capture current status before update
        old_status = self.get_object().status
        # Save the updated order
        order = serializer.save()
        
        #  Apply quantity changes if status changed to COMPLETED
        self.update_order(order)
        
        # Create notification for buyer if status changed
        if old_status != order.status:
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
    
        
        return notification
    
    def update_order(self, order):
        """Update order and adjust medicine quantities"""
        if order.status == Buy_Order.Choices.COMPLETED:
            
            medicine = order.medicine_name  # Get related medicine instance
            new_quantity = medicine.quantity_to_sell - order.quantity
            
            if new_quantity < 0:
                raise PermissionDenied("Insufficient quantity available for this order.")
  
                    
            # Update the exchange medicine quantity        
            medicine.quantity_to_sell = new_quantity
            medicine.save(update_fields=["quantity_to_sell"])
            
            # Update the exchange medicine entry
            exchange_entry = ExchangeMedciene.objects.filter(
                medicine=medicine, 
                operation=ExchangeMedciene.Status.SELL).first()

            if exchange_entry:
                exchange_entry.quantity = new_quantity
                exchange_entry.save(update_fields=["quantity"])
            
        
        return order

    
class Notification_View(generics.ListAPIView):
    serializer_class = NotificatoinSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [PharmacyJWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        pharmacy = getattr(self.request, "pharmacy", None)
        pharmacy_id = self.kwargs.get("pharmacy_id")  # Optional for owner

        if pharmacy:
            # Pharmacy staff access
            qs = Notification.objects.filter(pharmacy=pharmacy)
            if not qs.exists():
                raise PermissionDenied("No notifications found for this pharmacy.")
            return qs

        elif hasattr(user, 'owner'):
            # Owner access: either specify a pharmacy_id, or list all
            if pharmacy_id:
                try:
                    pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner=user.owner)
                except Pharmacy.DoesNotExist:
                    raise PermissionDenied("Pharmacy not found or not owned by you.")
                qs = Notification.objects.filter(pharmacy=pharmacy)
            else:
                qs = Notification.objects.filter(pharmacy__owner=user.owner)

            if not qs.exists():
                raise PermissionDenied("No notifications found for your pharmacies.")
            return qs

        raise PermissionDenied("Only pharmacy staff or owners can view notifications.")

  
class SubscriptionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Supports both owner & staff

    def perform_create(self, serializer):
        user = self.request.user
        token = self.request.auth  # This is the JWT token
        pharmacy_id = self.kwargs.get("pharmacy_id")

        # ✅ Case 1: Staff - pharmacy_id comes from token
        token_pharmacy_id = None
        if token and hasattr(token, 'payload'):
            token_pharmacy_id = token.payload.get("pharmacy_id")

        if token_pharmacy_id:
            try:
                pharmacy = Pharmacy.objects.get(id=token_pharmacy_id, owner__user=user)
                serializer.save(pharmacy=pharmacy)
                return
            except Pharmacy.DoesNotExist:
                raise PermissionDenied("Invalid token: Pharmacy not found or not owned by user.")

        # ✅ Case 2: Owner - pharmacy_id must be passed in URL
        elif hasattr(user, 'owner'):
            if not pharmacy_id:
                raise PermissionDenied("Owner must specify pharmacy_id in the URL.")
            try:
                pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner=user.owner)
                serializer.save(pharmacy=pharmacy)
                return
            except Pharmacy.DoesNotExist:
                raise PermissionDenied("Pharmacy not found or not owned by you.")

        # ❌ Not allowed
        raise PermissionDenied("Only pharmacy staff or owners can subscribe.")


class UserPurchaseView(generics.CreateAPIView):
    serializer_class = UserPurchaseSerializer