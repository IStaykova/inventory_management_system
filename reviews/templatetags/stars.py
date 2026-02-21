from django import template

register = template.Library()

@register.filter
def stars(rating):
    try:
        r=int(rating)
    except (TypeError, ValueError):
        r=0
    r = max(0, min(5, r))
    return "★" * r + "☆" * (5-r)