from studserviceapp_api.serializers.predmet_serializer import PredmetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from studserviceapp import korisne_funkcije


@api_view(['GET'])
def getAllPredmeti(request):
    predmeti = korisne_funkcije.vrati_predmete_tekuceg_semestra()
    json =  JSONRenderer().render(PredmetSerializer(predmeti, many=True).data)
    return HttpResponse(json)


