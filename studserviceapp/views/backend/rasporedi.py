from studserviceapp_api.serializers.raspored_serializer import TerminSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from studserviceapp import korisne_funkcije


@api_view(['GET'])
def prikazRasporeda(request):
    termini = korisne_funkcije.svi_termini_tekuceg_rasporeda()
    serializer = TerminSerializer(termini, many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)