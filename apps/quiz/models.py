from django.db import models


class Category(models.Model):
    """
    Категории вопросов.
    """
    name = models.CharField("Название категории", max_length=255)

    is_active = models.BooleanField("Активна ли категория?", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Question(models.Model):
    """
    Вопрос.
    """
    DEGREE_JUNIOR = 1  # Юнион
    DEGREE_MIDDLE = 2  # Middle
    DEGREE_SENIOR = 3  # Senior
    DEGREE_OTHER = 4  # Общие вопросы
    DEGREE_CHOICES = (
        (DEGREE_JUNIOR, "Junior"),
        (DEGREE_MIDDLE, "Middle"),
        (DEGREE_SENIOR, "Senior"),
        (DEGREE_OTHER, "Other")
    )
    TYPE_SINGLE = 1
    TYPE_MANY = 2
    TYPES = (
        (TYPE_SINGLE, "Один правильный ответ."),
        (TYPE_MANY, "Несколько правильных ответов.")
    )

    degree = models.PositiveSmallIntegerField("Сложность вопроса", choices=DEGREE_CHOICES, default=DEGREE_OTHER)
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="questions")
    # types = models.PositiveSmallIntegerField("Тип вопроса", choices=TYPES, default=TYPE_SINGLE)

    question = models.TextField("Вопрос")

    is_active = models.BooleanField("Доступен ли вопрос?", default=False)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return "{} {} {}".format(self.category, self.get_degree_display(), self.pk)

    def __repr__(self):
        return self.__str__()


class Answer(models.Model):
    """
    Вариант ответа на вопрос.
    """
    question = models.ForeignKey(Question, related_name="answers")
    answer = models.TextField("Ответ.")

    is_valid = models.BooleanField("Правильный ли ответ?", default=False)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return "{} {}".format(self.question, self.answer)

    def __repr__(self):
        return self.__str__()


class TestCase(models.Model):
    """
    Сам тест.
    """
    name = models.CharField("Название теста", max_length=255, blank=True)

    is_active = models.BooleanField("Активен ли тест?", default=False)

    time_to_test = models.DurationField("Время на тест")

    questions = models.ManyToManyField(Question, verbose_name="Вопросы на тест", related_name="test_case")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return "{} {}".format(self.name, self.time_to_test)

    def __repr__(self):
        return self.__str__()


class AccountTest(models.Model):
    """
    Аккаунт для тестирования.
    """
    name = models.CharField("ФИО тестируемого", max_length=255)
    email = models.EmailField("Email тестируемого")
    information = models.TextField("Дополнительная информация по тестируемуму", blank=True)
    
    password = models.CharField("Пароль для вхождения в тест", max_length=255)

    tests = models.ManyToManyField(TestCase, verbose_name="Тесты для пользователя", related_name="account_test")

    class Meta:
        verbose_name = "Аккаунт для тестирования"
        verbose_name_plural = "Аккаунты для тестирования"

    def __str__(self):
        return "{} {}".format(self.name, self.email)

    def __repr__(self):
        return self.__str__()


class Test(models.Model):
    """
    Процесс тестирования.
    """
    account = models.ForeignKey(AccountTest, verbose_name="Аккаунт для тестирования", related_name="account_test_result")
    test_case = models.ForeignKey(TestCase, verbose_name="Конкретный тест", related_name="testcase_test_result")

    date_start = models.DateTimeField("Дата начала тестирования", auto_now_add=True)
    date_end = models.DateTimeField("Дата окончания тестирования", null=True, blank=True)

    answers = models.TextField("Ответы аккаунта в формате JSON", blank=True)

    class Meta:
        verbose_name = "Тест для пользователя"
        verbose_name_plural = "Тесты для пользователя"

    def __str__(self):
        return "{} {} ({}-{})".format(
            self.account, self.test_case, self.date_start, self.date_end
        )

    def __repr__(self):
        return self.__str__()
