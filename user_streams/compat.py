try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    # Compat with previous 1.3 behavior
    from datetime import datetime
    from django.conf import settings
    if getattr(settings, 'USER_STREAMS_USE_UTC', False):
        datetime_now = datetime.utcnow
    else:
        datetime_now = datetime.now
