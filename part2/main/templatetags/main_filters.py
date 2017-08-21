from django import template

from main.dictionaries import area_names

register = template.Library()


@register.filter(name='getattr')
def getattribute(value, arg):
    attr = getattr(value, arg)
    if callable(attr):
        attr = attr()
    return attr


@register.filter(name='get')
def get(dic, key):
    return dic.get(key)
