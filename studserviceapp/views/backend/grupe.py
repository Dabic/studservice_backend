from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from studserviceapp import korisne_funkcije
from studserviceapp.models import IzbornaGrupa, Semestar, Predmet, Student

from studserviceapp_api.serializers.izbornagrupa_serializer import IzbornaGrupaSerializer
from studserviceapp_api.serializers.student_serializer import StudentSerializer
from studserviceapp_api.serializers.grupa_serializer import GrupaSerializer
from collections import defaultdict
import json as js


@api_view(['GET'])
def getAllIzborneGrupe(request):
    podaci = korisne_funkcije.vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=podaci[0], skolska_godina_pocetak=podaci[1], skolska_godina_kraj=podaci[2],
                                    aktivan=True)
    grupe = IzbornaGrupa.objects.filter(za_semestar=semestar)
    json = JSONRenderer().render(IzbornaGrupaSerializer(grupe, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
def getAllGrupeSaStudentima(request):
    grupe = korisne_funkcije.vrati_grupe_tekuceg_semestra()
    studenti_po_grupama = defaultdict(list)
    json = []
    for grupa in grupe:
        studenti_grupe = Student.grupa.through.objects.filter(grupa_id=grupa.id)
        for st_grupa in studenti_grupe:
            gr_serialized = GrupaSerializer(grupa).data
            studenti_po_grupama[JSONRenderer().render(gr_serialized)].append(
                StudentSerializer(Student.objects.get(id=st_grupa.student_id)).data)

    for key in studenti_po_grupama:
        print(key)
        json.append({"grupa": js.loads(key), "studenti": studenti_po_grupama[key]})
    json_end = JSONRenderer().render(json)
    return Response(json, status.HTTP_200_OK)
