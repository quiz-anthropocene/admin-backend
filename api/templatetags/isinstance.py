from django import template

register = template.Library()


@register.filter(name="isinstance")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))
