"""
Типы для GraphQL.

"""
import logging

import graphene
from graphene_django.types import DjangoObjectType

from apps.utils.graphql.fields import CustomDurationField

from ..models import Test, AccountTest, TestCase, Answer, Question


logger = logging.getLogger(__name__)


class AnswerTypeRead(DjangoObjectType):
    """
    Тип ответа для чтения. Для списка вопросов.

    """
    class Meta:
        model = Answer
        exclude_fields = ("is_valid",)


class AnswerTypeWrite(DjangoObjectType):
    """
    Тип ответа для записи. Для отправки на проверку.

    """
    class Meta:
        model = Answer
        only_fields = ("answer", "question")


class QuestionType(DjangoObjectType):
    """
    Тип вопроса для тестирования.

    """
    category = graphene.String()
    answers = graphene.List(AnswerTypeRead)

    class Meta:
        model = Question

    def resolve_answers(self, args, context, info):
        """
        Достаем варианты ответов.

        :param args: Аргументы к типу.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Queryset(Answers)
        :rtype: Queryset

        """
        return Answer.objects.filter(question=self)

    def resolve_category(self, args, context, info):
        """
        Достаем категорию.

        :param args: Аргументы к типу.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Category.name
        :rtype: str

        """
        return self.category.name


class TestCaseListType(DjangoObjectType):
    """
    Тип для списка доступных тестов.

    """
    time_to_test = CustomDurationField(description="Время на тест.")

    class Meta:
        model = TestCase
        only_fields = ("id", "name", "time_to_test")


class AccountTestType(DjangoObjectType):
    """
    Аккаунт пользователя.

    """
    tests = graphene.List(TestCaseListType)

    class Meta:
        model = AccountTest
        only_fields = ("name", "email", "tests")

    def resolve_tests(self, args, context, info):
        """
        Достаем тесты.

        :param args: Аргументы к типу.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Аккаунт или None
        :rtype: AccountTest

        """
        return self.tests.all()


class TestCaseInterface(graphene.Interface):
    """
    Интерфейс для самого теста.

    """
    status_test = graphene.String()
    time_to_test = CustomDurationField(description="Время на тест.")

    def resolve_status_test(self, args, context, info):
        """
        Смотрим статус теста по отношению к ползователю.

        :param args: Аргументы к типу.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Статус теста
        :rtype: str

        """
        if not hasattr(context, "account_test"):
            return None

        try:
            test = Test.objects.get(
                account=context.account_test,
                test_case=self
            )
        except Test.DoesNotExist as e:
            logger.error(e)
            return None
        except Test.MultipleObjectsReturned as e:
            logger.error(e)
            return None

        if test.date_end:
            return "Вы уже проходили тест."
        elif test.date_start:
            return "Сейчас невозможно начать сначала тест."

        return "Все готово для начала теста."


class TestCaseType(DjangoObjectType):
    """
    Тип для самого теста.

    """
    class Meta:
        interfaces = (TestCaseInterface,)
        model = TestCase
        exclude_fields = ("is_active", "questions")


class StartTestType(DjangoObjectType):
    """
    Тип для начала тестирования. Содержит тест для пользователя.

    """
    questions = graphene.List(QuestionType)

    class Meta:
        interfaces = (TestCaseInterface,)
        model = TestCase
        exclude_fields = ("is_active", "questions")

    def resolve_questions(self, args, context, info):
        """
        Получаем список вопросов на тест.

        :param args: Аргументы к типу.
        :param context: Request объект.
        :param info: AST запроса.
        :type args: dict
        :type context: django.core.handlers.wsgi.WSGIRequest
        :type info: graphql.execution.base.ResolveInfo

        :return: Список Question
        :rtype: Queryset

        """
        return self.questions.all()
