from django import template

register = template.Library()

@register.filter
def has_attribute(obj, attr):
    """Check if an object has a given attribute"""
    return hasattr(obj, attr)
