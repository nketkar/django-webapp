from django.conf import settings
from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'app', 'geokey.urls', name='app'),
    host(r'www', 'main.frontpage_urls', name='frontpage'),
)