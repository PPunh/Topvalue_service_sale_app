from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
from .models import User

class MultiAuthBackend(ModelBackend):
    '''
    custom Authentication so that we can login using
    username/password or email/password or phone_number/password
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        if "@" in username:  # Treat as email
            kwargs = {'email': username}
        elif username.isdigit(): # Treat as phone number
            kwargs = {'phone_number': username}
        else: # Treat as username
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
