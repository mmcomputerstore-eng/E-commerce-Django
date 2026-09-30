from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def filter_url(context, **kwargs):
    """
    Builds a query string by preserving current GET parameters while updating or removing specified ones.
    
    Usage:
        {% filter_url category=c.cid %}
        {% filter_url category='' %}           (removes category)
        {% filter_url vendor=v.vid %}
        {% filter_url min_price='' max_price='' %} (clears price)
    
    Returns:
        '?key1=val1&key2=val2' or '' if empty.
    """
    request = context.get('request')
    if not request:
        return ''

    params = request.GET.copy()

    # Changing any filter should reset pagination to the first page
    params.pop('page', None)

    for key, value in kwargs.items():
        if value is None or value == '' or value is False:
            params.pop(key, None)
        else:
            params[key] = str(value)

    # Filter out empty or whitespace-only keys/values
    cleaned = {k: v for k, v in params.items() if v is not None and str(v).strip() != ''}

    encoded = urlencode(cleaned)
    if encoded:
        return mark_safe(f'?{encoded}')
    return ''
