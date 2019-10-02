from rest_framework import permissions
from rest_framework.parsers import JSONParser
import requests
import io
from studserviceapp.models import Nalog


class AdminPermission(permissions.BasePermission):
    message = 'Not authorized.'

    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
        except KeyError:
            return False
        response = JSONParser().parse(io.BytesIO(
            requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + token).content))
        try:
            mail = response['email'].split('@')[0]
        except KeyError:
            return False
        try:
            nalog = Nalog.objects.get(username=mail)
            return nalog.uloga == 'Administrator'
        except Nalog.DoesNotExist:
            return False
