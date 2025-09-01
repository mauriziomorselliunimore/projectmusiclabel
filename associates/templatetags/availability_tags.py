from django import template

register = template.Library()

@register.filter
def filter_by_day(slots, day_num):
    return slots.filter(day_of_week=day_num)
