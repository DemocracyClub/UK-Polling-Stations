from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed


class ReadOnlyTokenAuthenticatedUser(AnonymousUser):
    def __init__(self, token):
        super().__init__()
        self.token = token

    @property
    def is_authenticated(self):
        return True

    @property
    def is_superuser(self):
        return False


class SuperTokenAuthenticatedUser(ReadOnlyTokenAuthenticatedUser):
    @property
    def is_superuser(self):
        return True


class HardcodedTokenAuthentication(ModelBackend):
    def authenticate(self, request, **kwargs):
        token: str = (
            request.GET.get("auth_token")
            or request.META.get("HTTP_AUTHORIZATION")
            or ""
        )
        token = token.removeprefix("Token ")
        if token in getattr(settings, "READ_ONLY_API_AUTH_TOKENS", []):
            user = ReadOnlyTokenAuthenticatedUser(token=token)
            return user, None
        if token in getattr(settings, "SUPERUSER_API_AUTH_TOKENS", []):
            user = SuperTokenAuthenticatedUser(token=token)
            return user, None
        raise AuthenticationFailed("Not a valid token")

    def authenticate_header(self, request):
        return "Token"
