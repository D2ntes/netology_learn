from django import template


register = template.Library()


@register.filter
def bgcolor(value):
    if value is '-':
        color = '#FFFFFF'
    else:
        if float(value) < 0:
            color = '#36C42A'
        elif 1 <= float(value) <= 2:
            color = '#F99A86'
        elif 2 < float(value) <= 5:
            color = '#E65C3F'
        elif float(value) > 5:
            color = '#C92B0A'
        else:
            color = '#FFFFFF'
    return color