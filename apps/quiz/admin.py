from django.contrib import admin

from .models import Category, Question, Answer, TestCase, AccountTest, Test
from .forms import AnswerBaseInlineFormSet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "name", "is_active"
    list_filter = "is_active",
    search_fields = "name",


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    min_num = 2
    formset = AnswerBaseInlineFormSet


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline, )
    list_display = "degree", "category", "is_active", "question"
    list_filter = "degree", "category", "is_active"
    search_fields = "category", "question"


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = "account", "test_case", "date_start", "date_end"
    list_filter = "test_case",
    search_fields = "account__name", "account__email", "test_case__name"
    readonly_fields = "account", "test_case", "date_start", "date_end", "answers"

    def save_model(self, request, obj, form, change):
        if change:
            obj.refresh_from_db()
        obj.save()

    def delete_model(self, request, obj):
        pass

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(TestCase)
class TeasCaseAdmin(admin.ModelAdmin):
    list_display = "name", "is_active", "time_to_test"
    list_filter = "is_active",
    search_fields = "name", "questions__question"
    filter_horizontal = "questions",


@admin.register(AccountTest)
class AccountAdmin(admin.ModelAdmin):
    list_display = "name", "email", "information"
    search_fields = "name", "email", "information"
    filter_horizontal = "tests",
