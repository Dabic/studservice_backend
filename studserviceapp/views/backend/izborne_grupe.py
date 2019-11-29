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
def get_izborne_grupe_godina(request, godina):
    izborne_grupe = IzbornaGrupa.objects.filter(oznaka_grupe__startswith=godina)
    json = JSONRenderer().render(IzbornaGrupaSerializer(izborne_grupe, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
@permission_classes([AdminPermission])
def get_all_izborne_grupe(request):
    izborne_grupe = IzbornaGrupa.objects.all()
    json = JSONRenderer().render(IzbornaGrupaSerializer(izborne_grupe, many=True).data)
    return HttpResponse(json)


@api_view(['POST'])
@permission_classes([AdminPermission])
def unos_izborne_grupe(request):
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
        return HttpResponse(js.dumps({'error': "Semestar za zadate parametre ne postoji! ({0}, {1}, {2})".format(
            semestar_vrsta, sk_pocetak, sk_kraj)}),
                            status=status.HTTP_400_BAD_REQUEST)
    if semestar_vrsta == "parni":
        oznaka_semestra = int(grupe[0]) * 2  # 1s2 = 1*2
    else:
        oznaka_semestra = int(grupe[0]) * 2 - 1

    grupe = grupe.split(',')
    for gr in grupe:
        try:
            test = IzbornaGrupa.objects.get(oznaka_grupe=gr, za_semestar=semestar)
            return HttpResponse(js.dumps({'error': 'Uneta grupa ' + gr + ' je pronadjena u bazi!'}),
                                status=status.HTTP_400_BAD_REQUEST)
        except IzbornaGrupa.DoesNotExist:
            izborna_grupa = IzbornaGrupa(oznaka_grupe=gr, oznaka_semestra=oznaka_semestra, kapacitet=kapacitet,
                                         smer=smer,
                                         aktivna=aktivnost == 'aktivna', za_semestar=semestar)
            izborna_grupa.save()
            novi_predmeti = [Predmet.objects.get(naziv=predmet['value']) for predmet in predmeti]
            izborna_grupa.predmeti.set(novi_predmeti)
            izborna_grupa.save()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AdminPermission])
def izmeni_izbornu_grupu(request):
    grupa = IzbornaGrupa.objects.get(id=request.data['id'])
    grupa.kapacitet = request.data['kapacitet']
    grupa.aktivna = request.data['aktivna']
    predmeti = [Predmet.objects.get(naziv=predmetNaziv['naziv']) for predmetNaziv in request.data['predmeti']]
    grupa.predmeti.set(predmeti)
    grupa.save()
    return HttpResponse(status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AdminPermission])
def obrisi_izbornu_grupu(request):
    IzbornaGrupa.objects.get(oznaka_grupe=request.data['oznaka_grupe']).delete()
    return HttpResponse(status.HTTP_200_OK)
