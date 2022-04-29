from django import template
from django.utils.encoding import force_str

from users import constants


register = template.Library()


@register.simple_tag
def array_choices_item_display(obj, field, value):
    """Pretty rendering of ArrayField value."""

    choices_dict = dict()

    if field == "roles":
        choices_dict = dict(constants.USER_ROLE_CHOICES)

    return force_str(choices_dict.get(value, ""))
