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

    try:
        nalog = Nalog.objects.get(username='dkostic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='dkostic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            print('usao')
            student = Student(ime='Darko',
                              prezime='Kostic',
                              broj_indeksa='84',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='ikocic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='ikocic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Irina',
                              prezime='Kocic',
                              broj_indeksa='84',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='ajokic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='ajokic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Ana',
                              prezime='Jokic',
                              broj_indeksa='85',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='mmicic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='mmicic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Mina',
                              prezime='Micic',
                              broj_indeksa='88',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='ncolic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='ncolic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Nina',
                              prezime='Colic',
                              broj_indeksa='89',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()


    try:
        nalog = Nalog.objects.get(username='lmilidrag17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='lmilidrag17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Lazar',
                              prezime='Milidrag',
                              broj_indeksa='90',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='mmladenovic17')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='mmladenovic17', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Mia',
                              prezime='Mladenovic',
                              broj_indeksa='91',
                              godina_upisa='2017',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='kmonteno70')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='kmonteno70', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Kemal',
                              prezime='Monteno',
                              broj_indeksa='92',
                              godina_upisa='1970',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()

    try:
        nalog = Nalog.objects.get(username='dmerlin90')
    except Nalog.DoesNotExist:
        nalog = Nalog(username='dmerlin90', lozinka='bla', uloga='student')
        nalog.save()
        grupa = Grupa.objects.get(oznaka_grupe='302', semestar=semestar)
        try:
            student = Student.objects.get(nalog_id=nalog.id)
        except Student.DoesNotExist:
            student = Student(ime='Dino',
                              prezime='Merlin',
                              broj_indeksa='93',
                              godina_upisa='1990',
                              smer='RN',
                              nalog=nalog)
            student.save()
            student = Student.objects.get(nalog=nalog)
            student.grupa.add(grupa)
            student.save()


scipt_popunjavanje_tima()


