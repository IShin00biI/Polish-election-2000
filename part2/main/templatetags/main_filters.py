from django import template

register = template.Library()


@register.filter(name='getattr')
def getattribute(value, arg):
    attr = getattr(value, arg)
    if callable(attr):
        attr = attr()
    return attr


@register.filter(name='verbose_name')
def verbose_name(value, arg):
    return value._meta.get_field_by_name(arg)[0].verbose_name
