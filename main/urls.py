from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from harness import EncodeAddressView, DecodeView, EncodePositionView, PrivateKeyset

from . import views


urlpatterns = [
    #url(r'^$', views.WelcomePageView.as_view(), name='welcome'),
    url(r'^$', views.UserGeoKeyCreateView.as_view(), name='usergeokey'),
    url(r'^please-subscribe$', views.SubscriptionNotificationView.as_view(), name='subscription_notification'),
    url(r'^geokey/email/(?P<geokey>[-\w\s]+)$', views.EmailGeoKeyFormView.as_view(), name='email_usergeokey'),
    url(r'^geokey/email/$', views.EmailGeoKeyFormView.as_view(), name='share_usergeokey'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url': 'login'}, name='logout'),
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
    url(r'^geokeys/$', views.UserGeoKeyListView.as_view(), name='usergeokeys'),
    url(r'^geokey/(?P<pk>[0-9]+)$', views.UserGeoKeyUpdateView.as_view(), name='usergeokey_update'),
    url(r'^geokey/(?P<pk>[0-9]+)/delete$', views.UserGeoKeyDeleteView.as_view(), name='usergeokey_delete'),
    url(r'^geokey/delete-all$', views.UserGeoKeyBulkDeleteView.as_view(), name='usergeokey_delete_all'),
    url(r'^searches/$', views.UserGeoKeyListMapView.as_view(), name='user_searches'),
    url(r'^searches/csv$', views.GeoKeyCSVView.as_view(), name='user_searches_csv'),
    url(r'^searches/excel$', views.GeoKeyExcelView.as_view(), name='user_searches_excel'),
    url(r'^from-address/$', EncodeAddressView.as_view(), name='from_address'),
    url(r'^from-geokey/$', DecodeView.as_view(), name='from_geokey'),
    url(r'^from-position/$', EncodePositionView.as_view(), name='from_position'),
    url(r'^keyset/$', PrivateKeyset.as_view(), name='keyset'),
    url(
        r'^activate/(?P<activation_key>[-:\w]+)$',
        views.UserActivationView.as_view(),
        name='activate_registration'
    ),
    url(r'^activate/fail/$', views.UserActivationFailureView.as_view(), name='activation_failure'),
    url(r'^password-reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(
        r'^reset/<uidb64>/<token>/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^password-reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^m/geokey/$', views.MobileGeoKeyView.as_view(), name='mobile_usergeokey'),
    url(r'^apple-app-site-association$', TemplateView.as_view(template_name="apple-app-site-association.txt", content_type="text/plain"), name="apple_file"),
    url(r'^share/$', views.ShareView.as_view(), name="share_geokey"),
]
