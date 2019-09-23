import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice_backend.settings")
import django

django.setup()

from studserviceapp.models import *
from studserviceapp import korisne_funkcije
def scipt_popunjavanje_tima():
    podaci_za_semestar = korisne_funkcije.vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=podaci_za_semestar[0],
                                    skolska_godina_pocetak=podaci_za_semestar[1],
                                    skolska_godina_kraj=podaci_za_semestar[2],
                                    aktivan=podaci_za_semestar[3])

    try:
        nalog = Nalog.objects.get(username='vdabic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='vdabic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='303', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            print('usao')
            student = Student(ime='Vladimir',
                              prezime='Dabic',
                              broj_indeksa='87',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='atomic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='atomic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            print('usao')
            student = Student(ime='Aleksandar',
                              prezime='Tomic',
                              broj_indeksa='83',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()



