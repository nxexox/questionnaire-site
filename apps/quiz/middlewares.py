"""
Миддлвары
"""
import logging

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .models import Token


logger = logging.getLogger(__name__)


class TestAccountMiddleware(MiddlewareMixin):
    """
    Крепит пользователя в request.

    """
    def process_request(self, request):
        """
        Пробуем достать токен из сессии, и получить по нему пользователя.

        :param request: Объект запроса
        :type request: django.http.request.HttpRequest

        """
        # if not request.user.is_authenticated:
        token_str = request.session.get("testing_auth_token", None)
        if token_str:
            try:
                token = Token.objects.get(token=token_str)
                request.account_test = token.account
            except Token.DoesNotExist as e:
                logger.error(e)
            except Token.MultipleObjectsReturned as e:
                logger.error(e)
