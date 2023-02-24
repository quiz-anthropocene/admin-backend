from django import template

from core import constants


register = template.Library()


@register.simple_tag
def get_language_flag(language):
    language_option = next(
        (language_option for language_option in constants.LANGUAGE_OPTIONS if language_option[2] == language["code"]),
        None,
    )
    if language_option:
        return language_option[3]
    return ""
