from django import template


register = template.Library()


@register.simple_tag
def highlight(request, path):
    if path in request.path:
        return 'active'
    else:
        return 'pass'
