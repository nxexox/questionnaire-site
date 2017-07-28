"""
Миддлвары
"""

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class TestAccountMiddleware(MiddlewareMixin):
    """
    Крепит пользователя в request.
    """

    def process_request(self, request):
        pass
