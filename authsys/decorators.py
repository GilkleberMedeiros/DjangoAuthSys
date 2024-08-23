from functools import wraps
from django.http import HttpResponseRedirect
from home.settings import NON_EMAIL_VALIDATED_USER_AGE, LOGIN_URL
from django.utils import timezone


def email_required(function = None, *, redirect_url = "/"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            user = request.user

            if user.id is None:
                return HttpResponseRedirect(LOGIN_URL)
            
            if user.is_superuser or user.is_staff:
                return func(*args, **kwargs)

            email_valid = user.email_validated

            td = timezone.now() - user.date_joined
            expired = td.total_seconds() * 1000 > NON_EMAIL_VALIDATED_USER_AGE

            if not email_valid and expired:
                return HttpResponseRedirect(redirect_url)
            
            return func(*args, **kwargs)

        return wrapper

    if function is None:
        return decorator
    
    return decorator(function)