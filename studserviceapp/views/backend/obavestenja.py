from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from django.shortcuts import HttpResponse
from studserviceapp.models import Obavestenje, Nalog
from django.utils import timezone

@api_view(['POST'])
def unos_obavestenja(request):
    [naslov, tekst, *_] = request.data
    file = request.data['file']
    obavestenje = Obavestenje()
    obavestenje.naslov = naslov
    obavestenje.tekst = tekst
    obavestenje.fajl = file
    obavestenje.datum_postavljanja = str(timezone.now())
    print('Postavio: autentifikovan korisinik treba da se doda')
    nalog = Nalog.objects.get(username='vdabic17')
    obavestenje.postavio = nalog
    obavestenje.save()
    return HttpResponse(status.HTTP_200_OK)