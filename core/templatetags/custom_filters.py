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
        return getattr(obj, f"get_{key}_display")
    except:  # noqa
        return obj.get(key)


@register.filter(name="get_list_item")
def get_list_item_filter(obj, index):
    """
    Find a dictionary value with a key as a variable.
    https://stackoverflow.com/a/8000091

    Usage:
        {% load custom_filters %}
        {{ list|get_list_item:index }}
    """
    try:
        return obj[index]
    except:  # noqa
        return {}


@register.filter(name="flatten_list")
def flatten_list(obj):
    if type(obj) is list:
        return ", ".join([str(item) for item in obj])
    return obj
