from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse
from rest_framework import status
from studserviceapp_api.serializers.izbornagrupa_serializer import IzbornaGrupaSerializer
from studserviceapp.models import IzbornaGrupa, Predmet, Semestar


@api_view(['GET'])
def vratiIzborneGrupe(request, godina):
    izborneGrupe = []
    if(godina != 'sve'):
        izborneGrupe = IzbornaGrupa.objects.filter(oznaka_grupe__startswith=godina)
    else:
        izborneGrupe = IzbornaGrupa.objects.all()
    json = JSONRenderer().render(IzbornaGrupaSerializer(izborneGrupe, many=True).data)
    return HttpResponse(json)


@api_view(['POST'])
def unosIzborneGrupe(request):
    [semestar_vrsta,
     sk_pocetak,
     sk_kraj,
     smer,
     grupe,
     kapacitet,
     predmeti,
     aktivnost] = request.data.values()
    semestar = Semestar.objects.get(vrsta=semestar_vrsta, skolska_godina_pocetak=sk_pocetak,
                                    skolska_godina_kraj=sk_kraj)
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
def obrisiIzbornuGrupu(request):
    oznaka_grupe = request.data['oznaka_grupe']
    #za_semestar = request.data['za_semestar']
    #Da li da getujem izbrone grupe za trenutni semestar ili nikada nece biti izbornih grupa iz proslog semestra?
    izborna = IzbornaGrupa.objects.get(oznaka_grupe=oznaka_grupe)
    izborna.delete()
    return HttpResponse(status.HTTP_200_OK)
