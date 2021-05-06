from datetime import datetime

from django import template
from jalali_date import datetime2jalali

register = template.Library()


@register.filter(name='convert_str_date')
def convert_str_date(value):
    try:
        return str(datetime2jalali(
            datetime.strptime(value, "%Y/%m/%d،\u200f %H:%M")
        ).strftime("%y/%m/%d %H:%M")
        )
    except Exception:
        return ''


@register.filter(name='value_or_null')
def value_or_null(value):
    if str(value) == "True":
        return "بله"
    elif str(value) == "False":
        return 'خیر'
    elif value is None:
        return ''
    return value
