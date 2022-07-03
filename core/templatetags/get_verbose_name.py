from django import template
from django.apps import apps
from django.utils.safestring import SafeString


register = template.Library()


@register.simple_tag
def get_verbose_name(object, field_name=None):
    if type(object) in [str, SafeString]:
        if object == "Question":
            object = apps.get_model("questions", object)
        elif object == "Quiz":
            object = apps.get_model("quizs", object)
        elif object == "Contribution":
            object = apps.get_model("contributions", object)
        elif object == "Glossaire":
            object = apps.get_model("glossary", "GlossaryItem")
    try:
        if field_name:
            # if 'verbose_name' is not defined, it will return the 'field_name'
            return object._meta.get_field(field_name).verbose_name
        else:
            return object._meta.verbose_name
    except:  # noqa
        return field_name
