from django.conf.urls import url, include
#from django.conf.urls import urls
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from views import ProfileView, UserGeoKeysViewSet, AuthCompleteView
from harness import DecodeView, EncodePositionView


#  Routers provide a way of automatically determining the URL conf.
#  router = routers.DefaultRouter()
#   router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^socialauthcomplete/$', AuthCompleteView.as_view(), name='socialauthcomplete'),
    url(r'^encode_geokey/$', EncodePositionView.as_view(), name='encode_geokey'),
    url(r'^decode_geokey/$', DecodeView.as_view(), name='decode_geokey'),
    url(r'^geokeys/(?P<pk>[0-9]+)/$', csrf_exempt(UserGeoKeysViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'})), name='user_geokey'),
    url(r'^geokeys/$', csrf_exempt(UserGeoKeysViewSet.as_view({'get': 'list', 'post':'create'})), name='user_geokeys'),
 #   url(r'oauth2/', include('social_django.urls', namespace='social')),
    # don't use login as name, it clashes with our other login view.
    url(r'^login/$', auth_views.login, name='api_login'),
]

 # Facebook login: https://app.geokey.io/api/oauth2/login/facebook/
 # Google login: https://app.geokey.io/api/oauth2/login/google-oauth2/?next=SOCIAL_LOGIN_REDIRECT_URL
 # http://localhost:8000/api/oauth2/login/google-oauth2/?next=SOCIAL_LOGIN_REDIRECT_URL
#
# """
# curl 'http://localhost:8000/api/profile/' \
# -H 'Accept: application/json' \
# -H 'Cookie: sessionid=wbeyzxlpk7ko7sers53vxzf23lbiqpns'
#
# curl 'http://localhost:8000/api/geokeys/' \
# -H 'Accept: application/json' \
# -H 'Cookie: sessionid=juapcidaac5oehiygnmgsrpicf36inrw'
#
# curl 'http://localhost:8000/api/decode_geokey/?geokey=HOOV%20NADA%20AIRN%20NADA' \
# -H 'Accept: application/json' \
# -H 'Cookie: sessionid=wbeyzxlpk7ko7sers53vxzf23lbiqpns'

# curl 'http://localhost:8000/api/decode_geokey/?geokey=HOOV%20NADA%20AIRN%20NADA'  -H 'Accept: application/json'  -H 'Cookie: sessionid=wbeyzxlpk7ko7sers53vxzf23lbiqpns'

#Create user geokey
#curl 'http://localhost:8000/api/geokeys/'  -H 'Accept: application/json'  -H 'Cookie: sessionid=juapcidaac5oehiygnmgsrpicf36inrw' -X POST -d '{"geokey":"AAAA BBBB", "nickname":"Home"}' -H "Content-Type: application/json"

#Edit user geokey
#curl 'http://localhost:8000/api/geokeys/5/' -H 'Accept: application/json'  -H 'Cookie: sessionid=juapcidaac5oehiygnmgsrpicf36inrw' -X PUT -d '{"geokey":"XXX", "nickname":"Home", "position":[46,46],"address":"3333"}' -H "Content-Type: application/json"

#Delete user geokey
#curl 'http://localhost:8000/api/geokeys/5/' -H 'Accept: application/json'  -H 'Cookie: sessionid=juapcidaac5oehiygnmgsrpicf36inrw' -X DELETE
