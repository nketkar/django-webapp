from django.conf import settings
from django.template import Library


register = Library()


@register.simple_tag(takes_context=True)
def absurl(context, path):
    """Returns an absolutized url for the given path"""
    if path.startswith('http'):
        return path
    try:
        return context['request'].build_absolute_uri(path)
    except KeyError:
        site = context.get('site', None)
        site_name = context.get('site_name', None)
        scheme = 'http' if settings.DEBUG else 'https'
        return "{scheme}://{root}{path}".format(
            scheme=scheme,
            root=site_name or site.domain,
            path=path
        )


@register.filter
def split(value, separator=' '):
    return value.split(separator)
