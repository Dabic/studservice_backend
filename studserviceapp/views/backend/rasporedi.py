from studserviceapp_api.serializers.raspored_serializer import TerminSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from studserviceapp_api.permissions import permissions
from django.shortcuts import HttpResponse
from studserviceapp import korisne_funkcije


@api_view(['GET'])
@permission_classes(
    [
        permissions.NastavnikPermission |
        permissions.StudentPermission |
        permissions.AdminPermission |
        permissions.SekretarPermission
    ]
)
def get_raspored_predavanja(request):
    termini = korisne_funkcije.svi_termini_tekuceg_rasporeda()
    serializer = TerminSerializer(termini, many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)


@api_view(['GET'])
@permission_classes(
    [
        permissions.NastavnikPermission |
        permissions.StudentPermission |
        permissions.AdminPermission |
        permissions.SekretarPermission
    ]
)
def get_raspored_ispita(request):
    pass


@api_view(['GET'])
@permission_classes(
    [
        permissions.NastavnikPermission |
        permissions.StudentPermission |
        permissions.AdminPermission |
        permissions.SekretarPermission
    ]
)
def get_raspored_kolokvijuma(request):
    termini = korisne_funkcije.svi_termini_tekuceg_rasporeda()
    serializer = TerminSerializer(termini, many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json)
