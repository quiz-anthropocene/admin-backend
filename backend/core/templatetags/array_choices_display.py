from django import template
from django.utils.encoding import force_str

from users import constants


register = template.Library()


@register.simple_tag
def array_choices_display(obj, field):
    """Pretty rendering of ArrayField with choices."""

    choices_dict = dict()

    if field == "roles":
        choices_dict = dict(constants.USER_ROLE_CHOICES)

    try:
        keys = obj.get(field, [])
    except:  # noqa
        keys = getattr(obj, field, [])

    value_display_list = [force_str(choices_dict.get(key, "")) for key in (keys or [])]
    return ", ".join(filter(None, value_display_list))
