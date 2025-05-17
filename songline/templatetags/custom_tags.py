from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def custom_range(value):
    return range(value)

@register.filter
def make_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()

@register.filter
def add_days(value, days):
    return value + timedelta(days=int(days))

@register.filter
def modulo(value, arg):
    return value % arg

@register.filter
def get_weekday_chinese(value):
    weekdays = ['日', '一', '二', '三', '四', '五', '六']
    return weekdays[value]