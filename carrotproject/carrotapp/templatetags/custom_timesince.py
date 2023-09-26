from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='custom_timesince')
def custom_timesince(value):
    now = timezone.now()
    difference = now - value
    
    days = difference.days
    seconds = difference.seconds
    minutes = seconds // 60
    hours = seconds // 3600
    weeks = days // 7
    
    if days >= 7:
        return f"{weeks}주 전"
    elif days >= 1:
        return f"{days}일 전"
    elif hours >= 1:
        return f"{hours}시간 전"
    elif minutes >= 1:
        return f"{minutes}분 전"
    else:
        return "방금 전"