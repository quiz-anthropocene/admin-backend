from django import template


register = template.Library()


@register.filter(name="isinstance")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))


@register.filter(name="get_obj_attr")
def get_obj_attr_filter(obj, key):
    """
    Find a dictionary value with a key as a variable.
    https://stackoverflow.com/a/8000091

    Usage:
        {% load custom_filters %}
        {{ instance|get_obj_attr:key }}
        {{ dict|get_obj_attr:key }}
    """
    try:
        value = getattr(obj, key)
    except:  # noqa
        value = obj.get(key)
    return value
