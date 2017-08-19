"""
Кастомные филды для GraphQL.

"""
import datetime

from django.conf import settings
from graphene.types.datetime import DateTime as GrapheneDateTime

SETTINGS = getattr(settings, "GRAPHENE", {})


class CustomDateTimeField(GrapheneDateTime):
    """
    Custom DateTimeFormat Scalar Type.

    """

    @staticmethod
    def serialize(dt):
        assert isinstance(dt, (datetime.datetime, datetime.date)), (
            'Received not compatible datetime "{}"'.format(repr(dt))
        )
        _format = SETTINGS.get("DATETIME_FORMAT", None)
        if _format:
            return dt.strftime(_format)

        return dt.isoformat()

    @staticmethod
    def parse_value(value):
        _format = SETTINGS.get("DATETIME_FORMAT", None)
        if _format:
            return datetime.datetime.strptime(value, _format)
        return super().parse_value(value)


class CustomDurationField(GrapheneDateTime):
    """
    Custom DurationField Scalar Type.

    """

    @staticmethod
    def serialize(dt):
        assert isinstance(dt, datetime.timedelta), (
            'Received not compatible datetime.timedelta "{}"'.format(repr(dt))
        )

        return str(dt)

    @staticmethod
    def parse_value(value):
        _format = SETTINGS.get("DATETIME_FORMAT", None)
        if _format:
            return datetime.datetime.strptime(value, _format)
        return super().parse_value(value)
