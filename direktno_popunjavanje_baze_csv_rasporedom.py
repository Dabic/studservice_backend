import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice_backend.settings")
django.setup()

from studserviceapp.models import *
from django.utils import timezone
from studserviceapp import korisne_funkcije


def popunjavanje_baze():
    with open("rasporedCSV.csv", encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        indeksPredavanja = 0
        indeksVezbi = 0
        indeksPraktikuma = 0
        indeksPredavanjaIPraktikuma = 0
        brojac = 0
        nazivPoslednjegPredmeta = ""
        podaci_tekuceg = korisne_funkcije.vrati_podatke_tekuceg_semestra()
        print("cao", podaci_tekuceg[0], podaci_tekuceg[1],podaci_tekuceg[2])
        try:  # uzimamo tekuci semestar iz baze, racunajuci da taj semestar postoji u bazi pre pravljenja rasporeda
            semestar = Semestar.objects.get(vrsta=podaci_tekuceg[0], skolska_godina_pocetak=podaci_tekuceg[1],
                                            skolska_godina_kraj=podaci_tekuceg[2], aktivan=True)
        except Semestar.DoesNotExist:
            semestar = Semestar(vrsta=podaci_tekuceg[0], skolska_godina_pocetak=podaci_tekuceg[1],
                                skolska_godina_kraj=podaci_tekuceg[2], aktivan=True)#promeniti ovo u jednom momentu zivota
            semestar.save()

        if not RasporedNastave.objects.filter(semestar=semestar).exists():
            raspored_nastave = RasporedNastave(semestar=semestar, datum_unosa=str(timezone.now()))
            raspored_nastave.save()
        else:
            print("Smisliti kako se hendluje ovaj slucaj: Vec postoji raspored za ovaj semestar")
            return 0

        for red in raspored_csv:
            if not red:
                continue
            else:
                if brojac == 0:
                    brojac += 1;
                    continue
                elif brojac == 1:
                    indeksPredavanja = red.index("Predavanja")
                    indeksPraktikuma = red.index("Praktikum")
                    indeksPredavanjaIPraktikuma = red.index("Predavanja i vezbe")
                    indeksVezbi = red.index("Vezbe")
                else:
                    if len(red) <= 2:  # predmet na nultom indeksu
                        try:
                            predmet = Predmet.objects.get(naziv=red[0])
                        except:
                            predmet = Predmet(naziv=red[0])
                            predmet.save()
                    else:
                        # termini nastave:
                        if red[1] == "Nastavnik(ci)":  # indeksi za to su vec obezbedjeni
                            brojac += 1
                            continue
                        else:
                            # ovo su cisti podaci o terminima
                            ############################################################################################
                            if red[indeksPredavanja] != '':
                                # prvo provera dal nastavnik vec postoji u bazi?
                                usernameNaloga = korisne_funkcije.napraviUsernameNaloga(red[indeksPredavanja])
                                # POSTOJI MOGUCNOST INDEXERROR-A, POPRAVITI TO! - napraviUsernName(samo ime/samo prezime)
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except Nalog.DoesNotExist:  # nalog ne postoji, pravim novog nastavnika i nalog
                                    nalog = Nalog(username=usernameNaloga, uloga="Nastavnik")
                                    nalog.save()
                                    tmp = red[indeksPredavanja].split()
                                    if len(tmp) > 2:
                                        nastavnik = Nastavnik(ime=tmp[2], prezime=tmp[0] + " " + tmp[1], nalog=nalog)
                                    else:
                                        nastavnik = Nastavnik(ime=tmp[1], prezime=tmp[0], nalog=nalog)
                                    nastavnik.save()
                                # dodavanje predmeta nastavniku, ako nastavnik vec nema taj predmet
                                if not predmet.nastavnik_set.filter(nalog=nalog).exists():
                                    nastavnik.predmet.add(predmet)
                                # pravljenje termina, dodavanje grupa
                                tmp = red[indeksPredavanja + 5].split('-')
                                termin = Termin(oznaka_ucionice=red[indeksPredavanja + 6], pocetak=tmp[0],
                                                zavrsetak=tmp[1] + ":00", dan=red[indeksPredavanja + 4],
                                                predmet=predmet, nastavnik=nastavnik, tip_nastave="Predavanja",
                                                raspored=raspored_nastave)
                                termin.save()
                                tmp = red[indeksPredavanja + 2].split(', ')  # grupe
                                for oznakaGrupe in tmp:
                                    try:
                                        grupa = Grupa.objects.get(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        termin.grupe.add(grupa)
                                    except Grupa.DoesNotExist:
                                        grupa = Grupa(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        grupa.save()
                                        termin.grupe.add(grupa)
                            ############################################################################################
                            if red[indeksVezbi] != '':
                                # prvo provera dal nastavnik vec postoji u bazi?
                                usernameNaloga = korisne_funkcije.napraviUsernameNaloga(red[indeksVezbi])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except Nalog.DoesNotExist:  # nalog ne postoji, pravim novog nastavnika i nalog
                                    nalog = Nalog(username=usernameNaloga, uloga="Nastavnik")
                                    nalog.save()
                                    tmp = red[indeksVezbi].split()
                                    if len(tmp) > 2:
                                        nastavnik = Nastavnik(ime=tmp[2], prezime=tmp[0] + " " + tmp[1], nalog=nalog)
                                    else:
                                        nastavnik = Nastavnik(ime=tmp[1], prezime=tmp[0], nalog=nalog)
                                    nastavnik.save()
                                # dodavanje predmeta nastavniku, ako nastavnik vec nema taj predmet
                                if not predmet.nastavnik_set.filter(nalog=nalog).exists():
                                    nastavnik.predmet.add(predmet)
                                # termini,grupe
                                tmp = red[indeksVezbi + 5].split('-')
                                termin = Termin(oznaka_ucionice=red[indeksVezbi + 6], pocetak=tmp[0],
                                                zavrsetak=tmp[1] + ":00", dan=red[indeksVezbi + 4], predmet=predmet,
                                                nastavnik=nastavnik, tip_nastave="Vezbe", raspored=raspored_nastave)
                                termin.save()
                                tmp = red[indeksVezbi + 2].split(', ')  # grupe
                                for oznakaGrupe in tmp:
                                    try:
                                        grupa = Grupa.objects.get(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        termin.grupe.add(grupa)
                                    except Grupa.DoesNotExist:
                                        grupa = Grupa(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        grupa.save()
                                        termin.grupe.add(grupa)
                            ############################################################################################
                            if red[indeksPraktikuma] != '':
                                # prvo provera dal nastavnik vec postoji u bazi?
                                usernameNaloga = korisne_funkcije.napraviUsernameNaloga(red[indeksPraktikuma])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except Nalog.DoesNotExist:  # nalog ne postoji, pravim novog nastavnika i nalog
                                    nalog = Nalog(username=usernameNaloga, uloga="Nastavnik")
                                    nalog.save()
                                    tmp = red[indeksPraktikuma].split()
                                    if len(tmp) > 2:
                                        nastavnik = Nastavnik(ime=tmp[2], prezime=tmp[0] + " " + tmp[1], nalog=nalog)
                                    else:
                                        nastavnik = Nastavnik(ime=tmp[1], prezime=tmp[0], nalog=nalog)
                                    nastavnik.save()
                                # dodavanje predmeta nastavniku, ako nastavnik vec nema taj predmet
                                if not predmet.nastavnik_set.filter(nalog=nalog).exists():
                                    nastavnik.predmet.add(predmet)
                                # termini, grupe
                                tmp = red[indeksPraktikuma + 5].split('-')
                                termin = Termin(oznaka_ucionice=red[indeksPraktikuma + 6], pocetak=tmp[0],
                                                zavrsetak=tmp[1] + ":00", dan=red[indeksPraktikuma + 4],
                                                predmet=predmet, nastavnik=nastavnik, tip_nastave="Praktikum",
                                                raspored=raspored_nastave)
                                termin.save()
                                tmp = red[indeksPraktikuma + 2].split(', ')  # grupe
                                for oznakaGrupe in tmp:
                                    try:
                                        grupa = Grupa.objects.get(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        termin.grupe.add(grupa)
                                    except Grupa.DoesNotExist:
                                        grupa = Grupa(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        grupa.save()
                                        termin.grupe.add(grupa)
                            ############################################################################################
                            if red[indeksPredavanjaIPraktikuma] != '':
                                # prvo provera dal nastavnik vec postoji u bazi?
                                usernameNaloga = korisne_funkcije.napraviUsernameNaloga(
                                    red[indeksPredavanjaIPraktikuma])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except Nalog.DoesNotExist:  # nalog ne postoji, pravim novog nastavnika i nalog
                                    nalog = Nalog(username=usernameNaloga, uloga="Nastavnik")
                                    nalog.save()
                                    tmp = red[indeksPredavanjaIPraktikuma].split()
                                    if len(tmp) > 2:
                                        nastavnik = Nastavnik(ime=tmp[2], prezime=tmp[0] + " " + tmp[1], nalog=nalog)
                                    else:
                                        nastavnik = Nastavnik(ime=tmp[1], prezime=tmp[0], nalog=nalog)
                                    nastavnik.save()
                                # dodavanje predmeta nastavniku, ako nastavnik vec nema taj predmet
                                if not predmet.nastavnik_set.filter(nalog=nalog).exists():
                                    nastavnik.predmet.add(predmet)
                                # termini, grupe
                                tmp = red[indeksPredavanjaIPraktikuma + 5].split('-')
                                termin = Termin(oznaka_ucionice=red[indeksPredavanjaIPraktikuma + 6], pocetak=tmp[0],
                                                zavrsetak=tmp[1] + ":00", dan=red[indeksPredavanjaIPraktikuma + 4],
                                                predmet=predmet, nastavnik=nastavnik, tip_nastave="Pred. i Vezbe",
                                                raspored=raspored_nastave)
                                termin.save()
                                tmp = red[indeksPredavanjaIPraktikuma + 2].split(', ')  # grupe
                                for oznakaGrupe in tmp:
                                    try:
                                        grupa = Grupa.objects.get(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        termin.grupe.add(grupa)
                                    except Grupa.DoesNotExist:
                                        grupa = Grupa(oznaka_grupe=oznakaGrupe, semestar=semestar)
                                        grupa.save()
                                        termin.grupe.add(grupa)
                            ############################################################################################
            brojac += 1


'''import timeit
t = timeit.Timer(setup='from csvParser import parsuj_csv_raspored', stmt='parsuj_csv_raspored()')'''
popunjavanje_baze()
