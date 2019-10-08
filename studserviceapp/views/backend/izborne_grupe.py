from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from studserviceapp_api.serializers.izbornagrupa_serializer import IzbornaGrupaSerializer
from studserviceapp_api.permissions.AdminPermission import AdminPermission
from studserviceapp.models import IzbornaGrupa, Predmet, Semestar
import json as js


@api_view(['GET'])
@permission_classes([AdminPermission])
def getIzborneGrupeGodina(request, godina):
    izborneGrupe = []
    izborneGrupe = IzbornaGrupa.objects.filter(oznaka_grupe__startswith=godina)
    json = JSONRenderer().render(IzbornaGrupaSerializer(izborneGrupe, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
@permission_classes([AdminPermission])
def getAllIzborneGrupe(request):
    izborneGrupe = []
    izborneGrupe = IzbornaGrupa.objects.all()
    json = JSONRenderer().render(IzbornaGrupaSerializer(izborneGrupe, many=True).data)
    return HttpResponse(json)


@api_view(['POST'])
@permission_classes([AdminPermission])
def unosIzborneGrupe(request):
    try:
        [semestar_vrsta,
         sk_pocetak,
         sk_kraj,
         smer,
         grupe,
         kapacitet,
         predmeti,
         aktivnost] = request.data.values()
    except ValueError:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        semestar = Semestar.objects.get(vrsta=semestar_vrsta, skolska_godina_pocetak=sk_pocetak,
                                        skolska_godina_kraj=sk_kraj)
    except Semestar.DoesNotExist:
        return HttpResponse(js.dumps({'error': "Semestar za zadate parametre ne postoji! ({0}, {1}, {2})".format(semestar_vrsta, sk_pocetak, sk_kraj)}),
                            status=status.HTTP_400_BAD_REQUEST)
    if semestar == "parni":
        oznaka_semestra = int(grupe[0]) * 2  # 1s2 = 1*2
    else:
        oznaka_semestra = int(grupe[0]) * 2 - 1

    grupe = grupe.split(',')
    for gr in grupe:
        try:
            test = IzbornaGrupa.objects.get(oznaka_grupe=gr, za_semestar=semestar)
            return HttpResponse(js.dumps({'error' : 'Uneta grupa ' + gr + ' je pronadjena u bazi!'}), status=status.HTTP_400_BAD_REQUEST)
        except IzbornaGrupa.DoesNotExist:
            izbornagrupa = IzbornaGrupa(oznaka_grupe=gr, oznaka_semestra=oznaka_semestra, kapacitet=kapacitet,
                                        smer=smer,
                                        aktivna=aktivnost == 'aktivna', za_semestar=semestar)
            izbornagrupa.save()
            for predmet in predmeti:
                izbornagrupa.predmeti.add(Predmet.objects.get(naziv=predmet['value']))
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AdminPermission])
def izmeniIzbornuGrupu(request):
    grupa = IzbornaGrupa.objects.get(id=request.data['id'])
    grupa.kapacitet = request.data['kapacitet']
    grupa.aktivna = request.data['aktivna']
    predmeti = []
    for predmetNaziv in request.data['predmeti']:
        predmeti.append(Predmet.objects.get(naziv=predmetNaziv['naziv']))
    grupa.predmeti.set(predmeti)
    grupa.save()
    return HttpResponse(status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AdminPermission])
def obrisiIzbornuGrupu(request):
    oznaka_grupe = request.data['oznaka_grupe']
    #za_semestar = request.data['za_semestar']
    #Da li da getujem izbrone grupe za trenutni semestar ili nikada nece biti izbornih grupa iz proslog semestra?
    izborna = IzbornaGrupa.objects.get(oznaka_grupe=oznaka_grupe)
    izborna.delete()
    return HttpResponse(status.HTTP_200_OK)
