from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]