from django import template
from django.http import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Preserva todos los parámetros GET existentes y actualiza/agrega los nuevos.
    
    Uso en template:
    {% url_replace page=2 %}
    """
    query = context['request'].GET.copy()
    
    for key, value in kwargs.items():
        query[key] = value
    
    return query.urlencode()