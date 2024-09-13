from rest_framework.authentication import BaseAuthentication
import jwt

from user.models import User
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        from config.settings.base import SECRET_KEY

        token = request.COOKIES.get('access')
        print(token)
        if not token:
            return None

        try:
            decode = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print(decode)
            user = User.objects.filter(id=decode['user_id']).first()
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return (user, None)
