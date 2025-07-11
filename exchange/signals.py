from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ExchangeMedciene

@receiver([post_save, post_delete], sender=ExchangeMedciene)
def invalidate_exchange_meds_cache(sender, instance, **kwargs):
    
    print("Clearing cache: Echange_list*")
    
    cache.delete_pattern('*exchange_med*')
