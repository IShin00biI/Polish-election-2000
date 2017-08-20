from django import template

register = template.Library()

@register.filter(name='getattr')
def getattribute(value, arg):
    return getattr(value, arg)
