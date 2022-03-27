from django import template


register = template.Library()


@register.filter(name="isinstance")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))


@register.filter(name="get_obj_attr")
def get_obj_attr_filter(obj, key):
    return getattr(obj, key)
