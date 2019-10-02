from django.urls import path
from studserviceapp.views.backend import rasporedi, predmeti, grupe, izborne_grupe, studenti, obavestenja, auth

urlpatterns = [
    # RASPORED
    path('raspored-predavanja/', rasporedi.getRasporedPredavanja),

    path('raspored-ispita/', rasporedi.getRasporedIspita),

    path('raspored-kolokvijuma/', rasporedi.getRasporedKolokvijuma),

    # IZBORNE GRUPE
    path('unos-grupe/', izborne_grupe.unosIzborneGrupe),

    path('obrisi-grupu/', izborne_grupe.obrisiIzbornuGrupu),

    path('izmeni-grupu/', izborne_grupe.izmeniIzbornuGrupu),

    path('izborne-grupe/<str:godina>/', izborne_grupe.getIzborneGrupe),

    # GRUPE
    path('grupe/', grupe.getAllGrupe),

    path('grupe/<str:godina>/', grupe.getGrupePoGodini),

    # STUDENTI
    path('studenti/', studenti.getAllStudenti),

    path('studenti/grupa/<str:grupa>/', studenti.getStudentiGrupa),

    path('studenti/godina/<str:godina>/', studenti.getStudentiGodina),

    # PREDMETI
    path('predmeti/', predmeti.getAllPredmeti),

    # OBAVESTENJA
    path('unos-obavestenja/', obavestenja.unos_obavestenja),

    # AUTORIZACIJA
    path('authorize/', auth.authorize),
]