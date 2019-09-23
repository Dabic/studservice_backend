from django.urls import path
from studserviceapp.views.backend import rasporedi, predmeti, grupe

urlpatterns = [
    path('raspored/', rasporedi.prikazRasporeda, name='book'),
    path('predmeti/', predmeti.getAllPredmeti, name='predmeti'),
    path('unos-grupe/', grupe.unos_grupe, name='unos_grupe'),
    path('izmena-grupe/', grupe.getAllIzborneGrupe, name='pregled-grupa'),
    path('obrisi-grupu/', grupe.obrisiGrupu, name='obrisi-grupu'),
]