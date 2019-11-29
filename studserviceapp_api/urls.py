from django.urls import path
from studserviceapp.views.backend import rasporedi, predmeti, grupe, izborne_grupe, studenti, obavestenja, auth, email

urlpatterns = [
    # RASPORED
    path('raspored-predavanja/', rasporedi.get_raspored_predavanja),

    path('raspored-ispita/', rasporedi.get_raspored_ispita),

    path('raspored-kolokvijuma/', rasporedi.get_raspored_kolokvijuma),

    # IZBORNE GRUPE
    path('unos-grupe/', izborne_grupe.unos_izborne_grupe),

    path('obrisi-grupu/', izborne_grupe.obrisi_izbornu_grupu),

    path('izmeni-grupu/', izborne_grupe.izmeni_izbornu_grupu),

    path('izborne-grupe/<str:godina>/', izborne_grupe.get_izborne_grupe_godina),

    path('izborne-grupe/', izborne_grupe.get_all_izborne_grupe),

    # GRUPE
    path('grupe/', grupe.get_all_grupe),

    path('grupe/<str:godina>/', grupe.get_grupe_po_godini),

    # STUDENTI
    path('studenti/', studenti.get_all_studenti),

    path('studenti/grupa/<str:grupa>/', studenti.get_studenti_grupa),

    path('studenti/godina/<str:godina>/', studenti.get_studenti_godina),

    # PREDMETI
    path('predmeti/', predmeti.get_all_predmeti),

    # OBAVESTENJA
    path('unos-obavestenja/', obavestenja.unos_obavestenja),

    # AUTORIZACIJA
    path('authorize/', auth.authorize),

    #EMAIL
    path('email-categories/', email.get_email_categories),
]