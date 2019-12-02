import requests
import io
from django.shortcuts import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from studserviceapp_api.serializers import grupa_serializer, predmet_serializer
from studserviceapp.models import Nalog, Predmet, Grupa, Nastavnik
from studserviceapp.korisne_funkcije import vrati_predmete_za_profesora, vrati_grupe_tekuceg_semestra_za_profesora
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from studserviceapp_api.permissions.AdminPermission import AdminPermission
from studserviceapp_api.permissions.SekretarPermission import SekretarPermission
from studserviceapp_api.permissions.NastavnikPermission import NastavnikPermission


@api_view(['POST'])

def send_email(request):
    response = JSONParser().parse(io.BytesIO(
        requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + request.headers['Authorization']).content))
    sender = response['email']
    # [to, cc, text, files] = request.data.values()
    print(sender, request.data['to'], request.data['cc'], request.data['heading'], request.data['text'])