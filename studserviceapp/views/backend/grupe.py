from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from studserviceapp import korisne_funkcije
from studserviceapp.models import IzbornaGrupa, Semestar, Predmet, Student, Grupa
from studserviceapp.korisne_funkcije import vrati_trenutni_semestar
from studserviceapp_api.serializers.student_serializer import StudentSerializer
from studserviceapp_api.serializers.grupa_serializer import GrupaSerializer
from studserviceapp_api.permissions import permissions


@api_view(['GET'])
@permission_classes([permissions.AdminPermission | permissions.SekretarPermission])
def get_grupe_po_godini(request, godina):
    grupa = Grupa.objects.filter(oznaka_grupe__startswith=godina, semestar=vrati_trenutni_semestar())
    json = JSONRenderer().render(GrupaSerializer(grupa, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
@permission_classes([permissions.AdminPermission | permissions.SekretarPermission])
def get_all_grupe(request):
    grupa = Grupa.objects.filter(semestar=vrati_trenutni_semestar())
    json = JSONRenderer().render(GrupaSerializer(grupa, many=True).data)
    return HttpResponse(json)
