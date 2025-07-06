from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_items(options_list):
    """Returns a dictionary mapping 'A', 'B', ... to options"""
    return dict(zip(['A', 'B', 'C', 'D'], options_list))
