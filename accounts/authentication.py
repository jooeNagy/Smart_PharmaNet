from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Pharmacy
import logging

logger = logging.getLogger(__name__)

class PharmacyJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if not result:
            logger.info("Authentication failed: No result")
            return None
        user, validated_token = result
        logger.info(f"Authenticated user: {user}, Token payload: {validated_token.payload}")
        pharmacy_id = validated_token.get('pharmacy_id')
        if pharmacy_id:
            try:
                pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner__user=user)
                logger.info(f"Staff login: User={user}, Pharmacy={pharmacy}")
                request.pharmacy = pharmacy
                return (user, validated_token)
            except Pharmacy.DoesNotExist:
                logger.error(f"Pharmacy {pharmacy_id} not found for user {user}")
                raise AuthenticationFailed('Invalid pharmacy ID or ownership')
        
        logger.info(f"Owner login: User={user}, No pharmacy_id")
        request.pharmacy = None
        return (user, validated_token)