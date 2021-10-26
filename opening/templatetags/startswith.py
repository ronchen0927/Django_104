from django import template
register = template.Library()

@register.filter
def str_startswith(s: str, starts: str):
    return s.startswith(starts)