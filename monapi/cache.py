from django.core.cache import cache
from django.conf import settings

CACHE_KEY_API_MONITOR_LIST = 'monitorlist:{:d}' # Format: monitorlist:{monitor_id}
CACHE_KEY_API_MONITOR_DETAIL_STATS = 'monitordetailstats:{:d}:{}' # Format: monitordetailstats:{monitor_id}:{range}
CACHE_KEY_API_MONITOR_STATS = 'monitorstats:{:d}' # Fromat: monitorstats:{user_id}

def get_cache_value(key):
    if not settings.CACHE_REDIS_ENABLED:
        return None
    return cache.get(key)

def set_cache_value(key, value, timeout=None):
    if not settings.CACHE_REDIS_ENABLED:
        return False
    return cache.set(key, value, timeout=timeout)
