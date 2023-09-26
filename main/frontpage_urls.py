from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.authtoken import views
#from django.urls import path, include
from . import views
from django.contrib import admin
from harness import EncodeAddressView, DecodeView, EncodePositionView, PrivateKeyset

urlpatterns = [
    url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
    url(r'^api/', include('api.urls')),
    url(r'^', include('main.urls')),
    #url(r'^api-token/', views.obtain_auth_token),
    url(r'^EncodeAddress/$', EncodeAddressView.as_view(), name='from_address'),
    url(r'^from-address/$', EncodeAddressView.as_view(), name='from_address'),
    url(r'^Decode/$', DecodeView.as_view(), name='from_geokey'),
    url(r'^from-geokey/$', DecodeView.as_view(), name='from_geokey'),
    url(r'^from-position/$', EncodePositionView.as_view(), name='from_position'),
    url(r'^EncodePosition/$', EncodePositionView.as_view(), name='from_position'),
    url(r'^CreatePrivateKeyset/$', PrivateKeyset.as_view(), name='keyset'),
    url(r'^keyset/$', PrivateKeyset.as_view(), name='keyset'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
