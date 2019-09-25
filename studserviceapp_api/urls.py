from django.urls import path
from studserviceapp.views.backend import rasporedi, predmeti, grupe, izborne_grupe, studenti

urlpatterns = [

    path('raspored/', rasporedi.prikazRasporeda),

    path('spisak-grupa/', grupe.getAllGrupeSaStudentima),

    path('unos-grupe/', izborne_grupe.unosGrupe),

    path('obrisi-grupu/', izborne_grupe.obrisiGrupu),

    path('izmeni-grupu/', izborne_grupe.izmeniGrupu),

    path('izborne-grupe/<str:godina>/', izborne_grupe.vratiIzborneGrupe),

    path('studenti/<str:tip>', studenti.getAllStudenti),

    path('predmeti/', predmeti.getAllPredmeti),

]