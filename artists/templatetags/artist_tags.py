from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter per accedere a un dizionario con una chiave variabile
    Uso: {{ mydict|get_item:key_var }}
    """
    return dictionary.get(key)
