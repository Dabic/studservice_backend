from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status

from studserviceapp import korisne_funkcije
from studserviceapp.models import IzbornaGrupa, Semestar, Predmet

from studserviceapp_api.serializers.izbornagrupa_serializer import IzbornaGrupaSerializer


@api_view(['GET'])
def getAllIzborneGrupe(request):
    podaci = korisne_funkcije.vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=podaci[0], skolska_godina_pocetak = podaci[1], skolska_godina_kraj=podaci[2], aktivan=True)
    grupe = IzbornaGrupa.objects.filter(za_semestar=semestar)
    json = JSONRenderer().render(IzbornaGrupaSerializer(grupe, many=True).data)
    return HttpResponse(json)

@api_view(['POST'])
def obrisiGrupu(request):
    print(request.data)
    oznaka_grupe = request.data['oznaka_grupe']
    za_smestar = request.data['za_semestar']
    izborna = IzbornaGrupa.objects.get(oznaka_grupe=oznaka_grupe)
    izborna.delete()
    return HttpResponse(status.HTTP_200_OK)

@api_view(['POST'])
def unos_grupe(request):
    [semestar_vrsta,
     sk_pocetak,
     sk_kraj,
     smer,
     grupe,
     kapacitet,
     predmeti,
     aktivnost] = request.data.values()
    print(sk_kraj)
    semestar = Semestar.objects.get(vrsta=semestar_vrsta, skolska_godina_pocetak=sk_pocetak, skolska_godina_kraj=sk_kraj)
    if semestar == "parni":
        oznaka_semestra = int(grupe[0]) * 2  # 1s2 = 1*2
    else:
        oznaka_semestra = int(grupe[0]) * 2 - 1

    grupe = grupe.split(',')
    for gr in grupe:
        izbornagrupa = IzbornaGrupa(oznaka_grupe=gr, oznaka_semestra=oznaka_semestra, kapacitet=kapacitet,
                                    smer=smer,
                                    aktivna=aktivnost == 'aktivna', za_semestar=semestar)
        izbornagrupa.save()
        for predmet in predmeti:
            izbornagrupa.predmeti.add(Predmet.objects.get(naziv=predmet['value']))
    return HttpResponse(status.HTTP_200_OK)

@api_view(['POST'])
def izmeni_grupu(request):
    grupa = IzbornaGrupa.objects.get(id = request.data['id'])
    grupa.kapacitet = request.data['kapacitet']
    grupa.aktivna = request.data['aktivna']
    predmeti = []
    for predmentNaziv in request.data['predmeti']:
        predmeti.append(Predmet.objects.get(naziv=predmentNaziv['naziv']))
    grupa.predmeti.set(predmeti)
    grupa.save()
    return HttpResponse(status.HTTP_200_OK)