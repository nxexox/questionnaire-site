"""
ALL Query для GraphQL.

"""
import logging
import datetime

import graphene
from graphql import GraphQLError

from .types import (
    AccountTestType, TestCaseType, StartTestType
)
from ..models import (
    AccountTest, TestCase, Test
)

logger = logging.getLogger(__name__)


class RootQuery(graphene.AbstractType, graphene.ObjectType):
    login = graphene.Field(
        AccountTestType,
        email=graphene.String(required=True),
        password=graphene.String(required=True)
    )  # Авторизация.
    user = graphene.Field(
        AccountTestType
    )  # Получить инфу по аккаунту.
    test = graphene.Field(
        TestCaseType,
        id=graphene.Int(required=True)
    )  # Получить тест для пользователя.
    start_test = graphene.Field(
        StartTestType,
        id=graphene.Int(required=True)
    )  # Начало тестирования.
    end_test = graphene.Field(
        TestCaseType,
        id=graphene.Int(required=True)
    )  # Завершение тестирования.

    def resolve_login(self, args, context, info):
        """
        Авторизация пользователя.

        :param args: Аргументы к ендпоинту.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Аккаунт или None
        :rtype: AccountTest

        """
        email, passwd = args.get("email"), args.get("password")
        accounts = AccountTest.objects.filter(email=email, password=passwd)

        if not accounts.exists():
            raise GraphQLError("Логин или пароль неверные.")

        account = accounts.first()

        context.session["testing_auth_token"] = account.get_auth_token()

        return account

    def resolve_user(self, args, context, info):
        """
        Возвращает авторизованный аккаунт для тестирования.

        :param args: Аргументы к ендпоинту.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Аккаунт или None
        :rtype: AccountTest

        """
        if hasattr(context, "account_test"):
            return context.account_test
        raise GraphQLError("Требуется авторизация.")

    def resolve_test(self, args, context, info):
        """
        Возвращает информацию по тесту, перед началом тестирования.

        :param args: Аргументы к ендпоинту.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Сам тест или None
        :rtype: TestCase

        """
        if not hasattr(context, "account_test"):
            raise GraphQLError("Требуется авторизация.")

        try:
            return context.account_test.tests.get(
                pk=args.get("id", None)
            )
        except TestCase.DoesNotExist as e:
            logger.error(e)
            raise GraphQLError("Такого теста не существует.")
        except TestCase.MultipleObjectsReturned as e:
            logger.error(e)
            raise GraphQLError("Произошла неизвестная ошибка.")

    def resolve_start_test(self, args, context, info):
        """
        Возвращает информацию по тесту, перед началом тестирования.

        :param args: Аргументы к ендпоинту.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Сам тест или None
        :rtype: TestCase

        """
        if not hasattr(context, "account_test"):
            raise GraphQLError("Требуется авторизация.")

        try:
            test_case = context.account_test.tests.get(
                pk=args.get("id", None)
            )  # Получили тест

            test = Test.objects.filter(test_case_id=args.get("id", None), account=context.account_test).first()
            if any([test.date_start, test.date_end, test.answers]):
                # Если пользователь его уже проходил.
                raise GraphQLError("Вы уже начинали тест с id `{}`.".format(args.get("id", "")))

            test.date_start = datetime.datetime.now()
            test.save()
            return test_case

        except TestCase.DoesNotExist as e:
            logger.error(e)
            raise GraphQLError("Такого теста не существует.")
        except TestCase.MultipleObjectsReturned as e:
            logger.error(e)
            raise GraphQLError("Произошла неизвестная ошибка.")


# TODO: Осталось написать проверку тест и ручку на результаты теста/ов
