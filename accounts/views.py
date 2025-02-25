from django.forms import ValidationError
from django.shortcuts import render
from .models import Owner, Pharmacy
from .serializers import OwnerSerializer, PharmacySerializer, EmailTokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
import logging


logger = logging.getLogger(__name__)
class OwnerRegisterView(generics.CreateAPIView):
    serializer_class = OwnerSerializer

    def create(self, request, *args, **kwargs):
        logger.info("request data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("validation error: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = super().create(request, *args, **kwargs)
            return result
        except Exception as e:
            print(f"Exception in create: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class PharmacyCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

    def perform_create(self, serializer):
        user = self.request.user
        try:
            owner = user.owner
            print(f'Creating Pharmacy for user: {owner}')
            serializer.save(owner=owner)
        except Owner.DoesNotExist:
            raise ValidationError({"details": "User has no associated Owner Account!"})
        
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomLogoutView(generics.GenericAPIView):
    # serializer_class = CustomLogoutSerializer
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            if not refresh:
                return Response({"error": "Refresh Token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh)
            OutstandingToken.objects.filter(token=token).delete()
            OutstandingToken.objects.filter(token=token.access_token).delete()
            return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)