from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.authtoken import views
#from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
    url(r'^api/', include('api.urls')),
    url(r'^', include('main.urls')),
    #url(r'^api-token/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
