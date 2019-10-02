from studserviceapp_api.serializers.predmet_serializer import PredmetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import HttpResponse
from studserviceapp import korisne_funkcije
from studserviceapp_api.permissions.AdminPermission import AdminPermission


@api_view(['GET'])
@permission_classes([AdminPermission])
def getAllPredmeti(request):
    predmeti = korisne_funkcije.vrati_predmete_tekuceg_semestra()
    json =  JSONRenderer().render(PredmetSerializer(predmeti, many=True).data)
    return HttpResponse(json)


