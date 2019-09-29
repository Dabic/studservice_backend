from django.urls import path
from studserviceapp.views.backend import rasporedi, predmeti, grupe, izborne_grupe, studenti, obavestenja, auth

urlpatterns = [

    path('raspored/', rasporedi.prikazRasporeda),

    path('unos-grupe/', izborne_grupe.unosIzborneGrupe),

    path('obrisi-grupu/', izborne_grupe.obrisiIzbornuGrupu),

    path('izmeni-grupu/', izborne_grupe.izmeniIzbornuGrupu),

    path('izborne-grupe/<str:godina>/', izborne_grupe.vratiIzborneGrupe),

    path('studenti/<str:tip>', studenti.getAllStudenti),

    path('grupe/<str:godina>/', grupe.vratiGrupe),

    path('predmeti/', predmeti.getAllPredmeti),

    path('unos-obavestenja/', obavestenja.unos_obavestenja),

    path('authorize/', auth.authorize),
]