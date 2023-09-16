from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from main.models import UserGeoKey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)


class AuthCompleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=request.user)
        redirect_url = '{}/authtoken/?token={}'.format(
            settings.NATIVE_APP_REDIRECT_URL, token.key) 
        response = Response(status=302)
        response['Location'] = redirect_url
        return response


class UserGeoKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGeoKey
        fields = ('id', 'created', 'geokey', 'nickname', 'position', 'address')


class UserGeoKeysViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserGeoKeySerializer

    def get_queryset(self):
        return UserGeoKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

