from django.forms import ValidationError
from django.shortcuts import render
from .models import Owner, Pharmacy
from .serializers import OwnerSerializer, PharmacySerializer, EmailTokenObtainPairSerializer, PharmacyLoginSerializer
from rest_framework import generics, status
from .permissions import IsOwner
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
    permission_classes = [IsOwner]
    serializer_class = PharmacySerializer

    def get_queryset(self):
        user = self.request.user
        try:
            owner = user.owner
            return Pharmacy.objects.filter(owner=owner)
        except Owner.DoesNotExist:
            raise ValidationError({"details": "User has no associated Owner account!"})

    def perform_create(self, serializer):
        user = self.request.user
        try:
            owner = user.owner
            serializer.save(owner=owner)
        except Owner.DoesNotExist:
            raise ValidationError({"details": "User has no associated Owner Account!"})
        

class PharmacyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PharmacySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Pharmacy.objects.filter(owner__user=self.request.user)
        

        

class LoginPharmacyView(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
        serializer = PharmacyLoginSerializer(data=request.data)
        if serializer.is_valid():
            pharmacy = serializer.validated_data['pharmacy']
            refresh = RefreshToken.for_user(pharmacy.owner.user)
            refresh['pharmacy_id'] = str(pharmacy.id)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "pharmacy": {
                    "id": pharmacy.id,
                    "name": pharmacy.name,
                    "license_number": pharmacy.license_number
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            refresh = request.data.get('refresh')
            if not refresh:
                return Response({"error": "refresh token is required!"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh)
            user = request.user
            
            pharmacy_id = token.get('pharmacy_id')
            if pharmacy_id:
                try:
                    pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner__user=user)
                    logger.info(f"Logging out pharmacy: {pharmacy.name}")
                except Pharmacy.DoesNotExist:
                    return Response({"error": "Invalid Pharmacy ID!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info("Logging out Owner!")
            
            OutstandingToken.objects.filter(user=user).delete()
            if pharmacy_id:
                return Response(
                    {"message": "Pharmacy logged out successfully!"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Owner logged out successfully!"},
                    status=status.HTTP_200_OK
                )
        
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
