from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class AnswerBaseInlineFormSet(BaseInlineFormSet):
    """ FormSet для списка ответов. """
    def clean(self):
        """ Смотрим что есть хотя бы один правильный ответ. """
        super(AnswerBaseInlineFormSet, self).clean()
        is_valid = False
        for form in self.forms:
            if not form.is_valid():
                return
            if not is_valid:
                is_valid = form.cleaned_data.get("is_valid", False)

        if not is_valid:
            raise ValidationError("Хотя бы один ответ должен быть правильный.")
