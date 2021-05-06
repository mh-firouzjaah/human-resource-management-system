from datetime import timedelta

from django import template

register = template.Library()


@register.filter(name='until_tomorrow')
def until_tomorrow(end, start):
    return 'روز بعد' if end == start + timedelta(days=1) else ''
