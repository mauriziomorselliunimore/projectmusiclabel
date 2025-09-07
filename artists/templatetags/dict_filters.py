from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Ottiene un elemento da un dizionario nel template.
    Uso: {{ my_dict|get_item:key }}"""
    return dictionary.get(key)
