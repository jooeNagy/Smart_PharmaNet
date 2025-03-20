from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

class IsOwner(BasePermission):

    def has_permission(self, request, view):
        # Allow GET requests (listing) for authenticated users
        if request.method == 'GET':
            return True
        # Deny POST (create) if request.pharmacy is set (staff token)
        if hasattr(request, 'pharmacy') and request.pharmacy is not None:
            logger.info("Denying create access: Pharmacy staff detected")
            raise PermissionDenied("You are not allowed to UPDATE or DELETE as a pharmacy staff!")
        logger.info("Allowing create access: Owner detected")
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if hasattr(request, 'pharmacy') and request.pharmacy is not None:
            logger.info("Denying access: Pharmacy staff detected")
            raise PermissionDenied("You are not allowed to UPDATE or DELETE as a pharmacy staff!")
        logger.info("Allowing access: Owner detected")
        return request.user == obj.owner.user