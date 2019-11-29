import requests
import io
from django.shortcuts import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from studserviceapp_api.serializers import grupa_serializer, predmet_serializer
from studserviceapp.models import Nalog, Predmet, Grupa, Nastavnik
from studserviceapp.korisne_funkcije import vrati_predmete_za_profesora, vrati_grupe_tekuceg_semestra_za_profesora
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def get_email_categories(request):
    response = JSONParser().parse(io.BytesIO(
        requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + request.headers['Authorization']).content))
    username = response['email'].split('@')[0]
    try:
        nalog = Nalog.objects.get(username=username)
    except Nalog.DoesNotExist:
        return HttpResponse({'error': 'Niste autoratizovani'}, status.HTTP_401_UNAUTHORIZED)
    data = {}
    if nalog.uloga == 'Administrator' or nalog.uloga == 'Sekretar':
        data = {
            'categories': [
                'Pojedinacno',
                'Po smeru',
                'Po grupama',
                'Po predmetima',
                'Po godinama',
                'Svi'
            ],
            'predmeti': predmet_serializer.PredmetSerializer(Predmet.objects.all(), many=True).data,
            'grupe': grupa_serializer.GrupaSerializer(Grupa.objects.all(), many=True).data,
            'smerovi': ['RN', 'RM'],
            'godine': ['I', 'II', 'III', 'IV']
        }
    elif nalog.uloga == 'Nastavnik':
        nastavnik = Nastavnik.objects.get(nalog_id=nalog.id)
        data = {
            'categories': [
                'Pojedinacno',
                'Po predmetima',
                'Po grupama'
            ],
            'predmeti': predmet_serializer.PredmetSerializer(vrati_predmete_za_profesora(nastavnik), many=True).data,
            'grupe': grupa_serializer.GrupaSerializer(vrati_grupe_tekuceg_semestra_za_profesora(nastavnik), many=True).data
        }
    json = JSONRenderer().render(data)
    return HttpResponse(json)