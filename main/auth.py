from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import SessionToken


class BearerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None

        token = header.removeprefix("Bearer ").strip()
        session = (
            SessionToken.objects
            .select_related("user", "user__role")
            .filter(token=token, is_active=True, expires_at__gt=timezone.now(), user__is_active=True)
            .first()
        )
        if not session:
            raise AuthenticationFailed("неверный или сломаный токен")

        return session.user, session
