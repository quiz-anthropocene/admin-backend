from django import template

from core.utils.utilities import remove_html_tags


register = template.Library()


@register.filter
def strip_html(text):
    return remove_html_tags(text)
