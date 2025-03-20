from django.utils.deprecation import MiddlewareMixin
import logging
from .models import Pharmacy

logger = logging.getLogger(__name__)

class PharmacyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if the token has pharmacy_id
            if hasattr(request, '_auth') and request._auth:  # _auth is the validated token
                pharmacy_id = request._auth.get('pharmacy_id')
                if pharmacy_id:
                    try:
                        pharmacy = Pharmacy.objects.get(id=pharmacy_id, owner__user=request.user)
                        request.pharmacy = pharmacy
                        logger.info(f"Middleware set request.pharmacy to {pharmacy}")
                    except Pharmacy.DoesNotExist:
                        request.pharmacy = None
                        logger.error(f"Pharmacy {pharmacy_id} not found")
                else:
                    request.pharmacy = None
                    logger.info("Middleware set request.pharmacy to None (owner)")
            else:
                request.pharmacy = None
                logger.info("Middleware set request.pharmacy to None (no token)")
        else:
            request.pharmacy = None
            logger.info("Middleware set request.pharmacy to None (unauthenticated)")