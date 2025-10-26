from typing import Any

from django import template
from django.http import QueryDict


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context: dict[str, Any], **kwargs: dict[str, Any]) -> QueryDict:
    """Replace or add query parameters in the current URL."""
    query = context["request"].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()
