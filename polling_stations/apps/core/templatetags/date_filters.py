import datetime as dt
from django import template
from django.template.defaultfilters import date

register = template.Library()


@register.filter
def human_date(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return date(value, "j F Y")
    elif isinstance(value, str):
        try:
            return date(dt.datetime.strptime(value, "%Y-%m-%d").date(), "j F Y")
        except ValueError:
            return value
    return value
