from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .models import Owner

@receiver(post_delete, sender=Owner)
def delete_owner_tokens(sender, instance, **kwargs):
    if hasattr(instance, 'user'):
        OutstandingToken.objects.filter(user=instance.user).delete()