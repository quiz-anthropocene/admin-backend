from django import template

# from questions.models import Question
# from quizs.models import Quiz
# from glossary.models import GlossaryItem
from django.apps import apps


register = template.Library()


@register.simple_tag
def get_verbose_name(object, field_name=None):
    if type(object) == str:
        if object == "Question":
            object = apps.get_model("questions", object)
        elif object == "Quiz":
            object = apps.get_model("quizs", object)
        elif object == "Glossaire":
            object = apps.get_model("glossary", "GlossaryItem")
    if field_name:
        # if 'verbose_name' is not defined, it will return the 'field_name'
        return object._meta.get_field(field_name).verbose_name
    else:
        return object._meta.verbose_name
