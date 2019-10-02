import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentski_servis.settings")
import django

django.setup()
from .models import *
from datetime import datetime
import csv
import codecs


class KljucRecnika(object):
    def __init__(self, name):
        self.name = name


generisane_moguce_ucionice = "rg1,Rg1,RG1,rg2,Rg2,RG2,rg3,Rg3,RG3,rg4,Rg4,RG4,rg5,Rg5,RG5,rg6,Rg6,RG6,rg7,Rg7,RG7,rg8,Rg8,RG8,rg9,Rg9,RG9,rg10,Rg10,RG10,rg11,Rg11,RG11,rg12,Rg12,RG12,Atelje,Kolarac"

def broj_studenata_grupe(grupa):
    student_grupa = Student.grupa.through.objects.filter(grupa_id=grupa.id)
    return len(student_grupa)

def vratiTrenutnuGrupuZaStudenta(student):
    student_grupa = Student.grupa.through.objects.filter(student_id=student.id)
    student_grupa = student_grupa.latest('id')
    grupa = Grupa.objects.get(id=student_grupa.grupa_id)
    return grupa

def napraviUsernameNaloga(imeiprezime):
    imeiprezime_pocetno = imeiprezime.split()
    imeiprezime = imeiprezime.split()
    duzina = len(imeiprezime)
    tmp = ""
    if duzina > 2:
        for iks in imeiprezime:
            if iks == imeiprezime[duzina - 1]:
                break
            else:
                tmp += iks
        imeiprezime = imeiprezime[duzina - 1][0] + tmp
        return imeiprezime.lower()
    else:
        imeiprezime = imeiprezime[1][0] + imeiprezime[0]

    imeiprezime_temp = imeiprezime.lower()
    if Nalog.objects.filter(username=imeiprezime_temp).exists():
        if not Nastavnik.objects.filter(ime=imeiprezime_pocetno[1], prezime=imeiprezime_pocetno[0]).exists():
            i = 1
            while True:
                imeiprezime_temp = imeiprezime + str(i)
                if not Nalog.objects.filter(username=imeiprezime_temp).exists():
                    break
                else:
                    i = i + 1
            return imeiprezime_temp.lower()
    return imeiprezime.lower()


def provera_kapaciteta_izborne_grupe(izborna_grupa):
    try:
        broj_upisanih_studenata = len(IzborGrupe.objects.filter(izabrana_grupa=izborna_grupa))
        return broj_upisanih_studenata
    except IzborGrupe.DoesNotExist:
        print("smisli sta vracas ako ne postoji")
        return False  # ?


def vrati_podatke_tekuceg_semestra():
    """vraca podatke o tekucem semestru u redosledu: vrsta, godina_poc, godina_kraj"""
    semestar = Semestar.objects.filter(aktivan=True).order_by('-id').first()  # ako ima više aktivnih (greska), ali vratice onaj sa najvecim id-jem, nema izuzetka
    if semestar is None:
        semestar = Semestar.objects.order_by('-id').first()  # ako nema aktivnog vraca onaj sa najvecim id-jem
    return (semestar.vrsta, semestar.skolska_godina_pocetak, semestar.skolska_godina_kraj, semestar.aktivan)   #ako ne postoji aktivan semestar ovo vraca None exception


def vrati_trenutni_semestar():
    semestar = Semestar.objects.filter(aktivan=True).order_by(
        '-id').first()  # ako ima više aktivnih (greska), ali vratice onaj sa najvecim id-jem, nema izuzetka
    if semestar is None:
        semestar = Semestar.objects.order_by('-id').first()
    return semestar


def vrati_raspored_nastave_tekuceg_semestra():
    """Vraca raspored nastave tekuceg semestra"""
    semestar = vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=semestar[0], skolska_godina_pocetak=semestar[1],
                                    skolska_godina_kraj=semestar[2])
    raspored_nastave = RasporedNastave.objects.get(semestar_id=semestar.id)
    return raspored_nastave


def svi_termini_tekuceg_rasporeda():
    raspored = vrati_raspored_nastave_tekuceg_semestra()
    termini_query_set = Termin.objects.filter(raspored=raspored)
    termini = []
    for termin in termini_query_set:
        termini.append(termin)
    return termini

def termini_tekuceg_rasporeda_za_profesora(nalog):
    raspored = vrati_raspored_nastave_tekuceg_semestra()
    nastavnik = Nastavnik.objects.get(nalog=nalog)
    termini_query_set = Termin.objects.filter(raspored=raspored,nastavnik=nastavnik)
    termini = []
    for termin in termini_query_set:
        termini.append(termin)
    return termini


def vrati_grupe_tekuceg_semestra():
    """Vraca grupe koje pripadaju tekucem semestru"""
    semestar = vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=semestar[0], skolska_godina_pocetak=semestar[1],
                                    skolska_godina_kraj=semestar[2])
    grupe = Grupa.objects.filter(semestar_id=semestar.id)
    return grupe


def vrati_predmete_tekuceg_semestra():
    """Vraca sve predmete koji pripadaju tekucem semestru"""
    raspored_nastave = vrati_raspored_nastave_tekuceg_semestra()
    termini = Termin.objects.filter(raspored_id=raspored_nastave.id)
    predmeti = []
    for termin in termini:
        predmet_temp = Predmet.objects.get(id=termin.predmet_id)
        if not predmeti.__contains__(predmet_temp):
            predmeti.append(predmet_temp)
    return predmeti


def vrati_predmete_za_profesora(nastavnik):
    nastavnik_predmet = Nastavnik.predmet.through.objects.filter(nastavnik_id=nastavnik.id)
    predmeti = []
    for predmet in nastavnik_predmet:
        predmeti.append(Predmet.objects.get(id=predmet.predmet_id))
    return predmeti


def vrati_grupe_tekuceg_semestra_za_profesora(nastavnik):
    raspored_nastave = vrati_raspored_nastave_tekuceg_semestra()
    termini = Termin.objects.filter(nastavnik_id=nastavnik.id)
    termin_grupe = []
    grupe = []
    for termin in termini:
        termin_grupe.append(Termin.grupe.through.objects.filter(termin_id=termin.id))
    for termini in termin_grupe:
        for grupa in termini:
            grupe.append(Grupa.objects.get(id=grupa.grupa_id))
    return grupe


# bds - proveravaju se samo nastavnici, predmeti, datumi i vreme
# ne snima se fajl
def ucitaj_raspored_kolokvijuma(raspored_fajl):

    raspored_csv = csv.DictReader(codecs.iterdecode(raspored_fajl, 'utf-8'), delimiter=',')
    broj_ispravnih_linja = 0
    broj_neispravnih_linija = 0
    objasnjenje_za_liniju = dict()  # redni broj linje : tekst objasnjenja
    redni_broj_linije = 1
    ispravne_linje = []
    neispravne_linije = []
    ispravni_termini = []
    for linija in raspored_csv:
            redni_broj_linije+=1
            #Predmet:
            try:
                predmet = Predmet.objects.get(naziv=linija['Predmet'])
            except Predmet.DoesNotExist:
                broj_neispravnih_linija +=1
                neispravne_linije.append(linija)
                objasnjenje_za_liniju[redni_broj_linije] = ("Predmet \"" + linija['Predmet']+ "\" nije pronadjen u bazi. ",linija)
                continue
            #Nastavnik
            try:
                nastavnici = []
                if ',' in linija['Profesor']:
                    nastavnici_imena = linija['Profesor'].split(",")
                    for n in nastavnici_imena:
                        ime_prezime = n.split(" ", 1)
                        if len(ime_prezime) < 2:
                            raise Nastavnik.DoesNotExists
                        nastavnici.append(Nastavnik.objects.get(ime=ime_prezime[0].strip(), prezime=ime_prezime[1].strip()))
                else:
                    ime_prezime = linija['Profesor'].split(" ",1)
                    if len(ime_prezime) < 2:
                        raise Nastavnik.DoesNotExists
                    nastavnik = Nastavnik.objects.get(ime=ime_prezime[0], prezime=ime_prezime[1])
                    nastavnici.append(nastavnik)

            except Nastavnik.DoesNotExist:
                broj_neispravnih_linija += 1
                neispravne_linije.append(linija)
                objasnjenje_za_liniju[redni_broj_linije] = ("Nastavnik \"" + linija['Profesor'] + "\" nije pronadjen u bazi. ",linija)
                continue
            # Vreme
            try:
                vremeOdDo = linija['Vreme'].split('-')
                pocetak = datetime.strptime(vremeOdDo[0], '%H')
                zavrsetak = datetime.strptime(vremeOdDo[1], '%H')
            except ValueError:
                broj_neispravnih_linija += 1
                neispravne_linije.append(linija)
                objasnjenje_za_liniju[redni_broj_linije] = ("Neispravan datum \"" + linija['Datum'] + "\"", linija)
                continue

            # Datum
            try:
                datum_odrzavanja = datetime.strptime(linija['Datum'], '%d.%m.%Y.')
            except ValueError:
                broj_neispravnih_linija += 1
                neispravne_linije.append(linija)
                objasnjenje_za_liniju[redni_broj_linije] = ("Neispravan datum \""+linija['Datum']+"\"",linija)
                continue
            broj_ispravnih_linja+=1 # ako se nije desio ni jedan izuzetak
            ispravne_linje.append(linija)
            # snimamo jo[ jednu strukturu pripremljenu za snimanje, za svakog nastavnika posebno
            termin = linija['Vreme'].split('-')
            for n in nastavnici:
                ispravni_termini.append({'predmet':predmet.id,'nastavnik':n.id, 'datum':datum_odrzavanja.strftime("%Y-%m-%d"),'ucionice':linija['Učionice'],
                                         'dan':linija['Dan'],'pocetak':pocetak.strftime("%H"),'zavrsetak':zavrsetak.strftime('%H')})
    return {'broj_ispravnih_linija':broj_ispravnih_linja, 'broj_neispravnih_linija':broj_neispravnih_linija,
            'objasnjenja_za_linije':objasnjenje_za_liniju,'ispravne_linije':ispravne_linje, 'ispravni_termini':ispravni_termini}


def sacuvaj_termine_polaganja(termini_polaganja, id_vazan_datum):
    vazan_datum = VazniDatumi.objects.get(id=id_vazan_datum)
    raspored_polaganja = RasporedPolaganja(vazan_datum=vazan_datum)
    raspored_polaganja.save()
    for t in termini_polaganja:
        predmet = Predmet.objects.get(id=t['predmet'])
        nastavnik = Nastavnik.objects.get(id=t['nastavnik'])

        termin = TerminPolaganja(raspored_polaganja=raspored_polaganja, predmet=predmet, nastavnik=nastavnik,
                                 ucionice=t['ucionice'], pocetak=datetime.strptime(t['pocetak'], '%H'),
                                 zavrsetak=datetime.strptime(t['zavrsetak'], '%H'), dan=t['dan'], datum=t['datum'])
        termin.save()


                # def ucitaj_raspored_kolokvijuma(importovani_fajl):
#     """ucitava TerminePolaganja u bazu i vraca:
#     1)Recnik cije su vrednosti linije ucitanog fajla, gde jedna linija predstavlja jedan termin polaganja,
#       a kljucevi obavestenje o greskama do kojih je doslo prilikom parsiranja ili obavestenje da su validne.
#       Takodje sadrzi i ukupan broj gresaka.
#     2)0 ako header fajla nije u ispravnom formatu
#     Ako recnik ostane prazan to znaci da su svi termini uspesno ucitani u bazu, odnosno da nije doslo do greske
#     """
#     with open("media/" + importovani_fajl.name, encoding='utf-8') as csvfile:
#         raspored_csv = csv.DictReader(csvfile, delimiter=',')
#         # prvo ide provera korektnosti prve linije da bismo izbegli KeyError pri uzimanju vrednosti kljuceva
#         validni_elementi = ["Predmet", "Profesor", "Učionice", "Vreme", "Dan", "Datum"]
#         if not all(element in raspored_csv.fieldnames for element in validni_elementi):
#             # ne sadrzi, vracam da je problem sa prvom linijom
#             return {"heder": "heder"}
#         linije_sa_obavestenjem = {}  # recnik koji ce kao kljuc imati greske koje se nalaze u liniji, a kao vrednost samu liniju
#         dani = ["Ponedeljak", "Utorak", "Sreda", "Četvrtak", "Cetvrtak", "Petak", "Subota", "Nedelja"]
#         redni_broj_linije = 2;
#         ukupan_broj_gresaka = 0
#         for linija in raspored_csv:
#             greske = ""
#             nema_greske = True  # ako se ne naidje na gresku, termin polaganja se moze ucitati u bazu
#             # Predmet:
#             try:
#                 predmet = Predmet.objects.get(naziv=linija['Predmet'])
#             except Predmet.DoesNotExist:
#                 greske += "Predmet \"" + linija['Predmet'] + "\" nije pronadjen u bazi. "
#                 nema_greske = False
#                 ukupan_broj_gresaka += 1
#                 continue   # bds: jer brojimo samo linije
#             # Profesor:
#             ime_prezime = linija['Profesor'].split(" ")
#             if len(ime_prezime) < 2:  # ako nedostaje ime ili prezime ne moramo proveravati u bazi
#                 greske += "Nastavnik \"" + linija['Profesor'] + "\" nije pronadjen u bazi|"
#                 nema_greske = False
#                 ukupan_broj_gresaka += 1
#                 continue
#             else:
#                 try:
#                     nastavnik = Nastavnik.objects.get(ime=ime_prezime[0], prezime=ime_prezime[1])
#                 except Nastavnik.DoesNotExist:
#                     greske += "Nastavnik \"" + linija['Profesor'] + "\" nije pronadjen u bazi. "
#                     nema_greske = False
#                     ukupan_broj_gresaka += 1
#                     continue
#             #
#             #ucionice = linija['Učionice'].split(',')
#             # for oznaka_ucionice in ucionice:
#             #     try:
#             #         if oznaka_ucionice not in generisane_moguce_ucionice:
#             #             broj = int(oznaka_ucionice)
#             #             if broj > 15 or broj < 1:
#             #                 greske += "Ucionice \"" + linija['Učionice'] + "\" se ne mogu parsirati. "
#             #                 nema_greske = False
#             #                 ukupan_broj_gresaka += 1
#             #                 break
#             #     except ValueError:
#             #         greske += "Ucionice \"" + linija['Učionice'] + "\" se ne mogu parsirati. "
#             #         nema_greske = False
#             #         ukupan_broj_gresaka += 1
#             #         break
#             # Vreme:
#             vreme = linija['Vreme'].split('-')
#             if len(vreme) != 2:
#                 greske += "Vreme \"" + linija['Vreme'] + " \"se ne moze parsirati. "
#                 nema_greske = False
#                 ukupan_broj_gresaka += 1
#                 continue
#             else:
#                 try:
#                     pocetak = int(vreme[0])
#                     zavrsetak = int(vreme[1])
#                     if pocetak < 0 or zavrsetak < 0 or pocetak > 23 or zavrsetak > 23 or pocetak >= zavrsetak or len(
#                             vreme[0]) != 2 or len(vreme[1]) != 2:
#                         greske += "Vreme \"" + linija['Vreme'] + " \"se ne moze parsirati. "
#                         nema_greske = False
#                         ukupan_broj_gresaka += 1
#                 except Exception:
#                     greske += "Vreme \"" + linija['Vreme'] + " \"se ne moze parsirati. "
#                     nema_greske = False
#                     ukupan_broj_gresaka += 1
#                     continue
#             # Dan:
#             if linija['Dan'] not in dani:
#                 greske += "Dan \"" + linija['Dan'] + "\" se ne moze parsirati. "
#                 nema_greske = False
#                 ukupan_broj_gresaka += 1
#             # Datum:
#             datum = linija['Datum'].split('.')
#             if len(datum) != 3:  # zbog poslednje tacke - 22.11.
#                 greske += "Datum \"" + linija['Datum'] + "\" se ne moze parsirati. "
#                 nema_greske = False
#                 ukupan_broj_gresaka += 1
#             else:
#                 if datum[2] != "" or len(datum[0]) != 2 or len(datum[1]) != 2:  # poslednja tacka
#                     greske += "Datum \"" + linija['Datum'] + "\" se ne moze parsirati. "
#                     nema_greske = False
#                     ukupan_broj_gresaka += 1
#                 else:
#                     try:
#                         dan = int(datum[0])
#                         mesec = int(datum[1])
#                         if dan < 0 or mesec < 0 or dan > 31 or mesec > 12:
#                             greske += "Datum \"" + linija['Datum'] + "\" se ne moze parsirati. "
#                             nema_greske = False
#                             ukupan_broj_gresaka += 1
#                     except ValueError:
#                         greske += "Datum \"" + linija['Datum'] + "\" se ne moze parsirati. "
#                         nema_greske = False
#                         ukupan_broj_gresaka += 1
#
#             if nema_greske:
#                 # modifikujem datum i vreme zbog template-a, vreme mora biti u formatu sati:minuta
#                 # datum mora biti u formatu yyyy-mm-dd a ne 22.11., i mora biti 01 a ne samo 1
#                 tmp = linija['Datum'].split('.')
#                 formatiran_datum = "" + str(datetime.now().year) + "-" + tmp[1] + "-" + tmp[0]
#                 tmp = linija['Vreme'].split('-')
#                 formatirani_sati_pocetka = tmp[0] + ":" + "00"
#                 formatirani_sati_zavrsetka = tmp[1] + ":" + "00"
#                 linije_sa_obavestenjem[KljucRecnika("Ispravna")] = [linija['Predmet'], linija['Profesor'],
#                                                                     linija['Učionice'], formatirani_sati_pocetka,
#                                                                     formatirani_sati_zavrsetka, linija['Dan'],
#                                                                     formatiran_datum]
#             else:
#                 # posto postoje greske, pre formatiranja se mora proveriti da li je do greske doslo u datumu/vremenu
#                 # ako jeste, vrednost linije_sa_obavestenjem moze imati linija['Datum'] (lose formatiran datum) jer
#                 # se on nece koristi u templejtu
#                 tmp = linija['Datum'].split('.')
#                 formatiran_datum = linija['Datum'] if "Datum" in greske else "" + str(datetime.now().year) + "-" + \
#                                                                              tmp[1] + "-" + tmp[0]
#                 tmp = linija['Vreme'].split('-')
#                 formatirani_sati_pocetka = linija['Vreme'] if "Vreme" in greske else tmp[0] + ":" + "00"
#                 formatirani_sati_zavrsetka = linija['Vreme'] if "Vreme" in greske else tmp[1] + ":" + "00"
#                 izvestaj = "Redni broj linije: " + str(redni_broj_linije) + ". Greske: " + greske
#                 linije_sa_obavestenjem[KljucRecnika(izvestaj)] = [linija['Predmet'], linija['Profesor'],
#                                                                   linija['Učionice'], formatirani_sati_pocetka,
#                                                                   formatirani_sati_zavrsetka, linija['Dan'],
#                                                                   formatiran_datum]
#
#             redni_broj_linije += 1
#
#         # jos da se prilepi koliko gresaka ima
#         linije_sa_obavestenjem[KljucRecnika("Ukupan broj gresaka")] = ukupan_broj_gresaka
#         return linije_sa_obavestenjem








def ucitaj_raspored_nastave(importovani_fajl, semestar, raspored_nastave):
    with open("media/" + importovani_fajl.name, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        indeksPredavanja = 0
        indeksVezbi = 0
        indeksPraktikuma = 0
        indeksPredavanjaIPraktikuma = 0
        brojac = 0
        podaci_tekuceg = vrati_podatke_tekuceg_semestra()
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
                            return "Predmet " + red[0] + " nije pronadjen u bazi"
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
                                usernameNaloga = napraviUsernameNaloga(red[indeksPredavanja])
                                # POSTOJI MOGUCNOST INDEXERROR-A, POPRAVITI TO! - napraviUsernName(samo ime/samo prezime)
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except (Nalog.DoesNotExist, Nastavnik.DoesNotExist) as e:
                                    return "Nastavnik " + red[indeksPredavanja] + " nije pronadjen u bazi"
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
                                usernameNaloga = napraviUsernameNaloga(red[indeksVezbi])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except (Nalog.DoesNotExist, Nastavnik.DoesNotExist) as e:
                                    return "Nastavnik " + red[indeksVezbi] + " nije pronadjen u bazi"
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
                                usernameNaloga = napraviUsernameNaloga(red[indeksPraktikuma])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except (Nalog.DoesNotExist, Nastavnik.DoesNotExist) as e:
                                    return "Nastavnik " + red[indeksPraktikuma] + " nije pronadjen u bazi"
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
                                usernameNaloga = napraviUsernameNaloga(
                                    red[indeksPredavanjaIPraktikuma])
                                try:
                                    nalog = Nalog.objects.get(username=usernameNaloga, uloga="Nastavnik")
                                    nastavnik = Nastavnik.objects.get(nalog=nalog)
                                except (Nalog.DoesNotExist, Nastavnik.DoesNotExist) as e:
                                    return "Nastavnik " + red[indeksPredavanjaIPraktikuma] + " nije pronadjen u bazi"
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
    return "Uspesno"

def vrati_termine_predavanja_za_ponovca(student):
    predmeti = []
    podaci_tekuceg = vrati_podatke_tekuceg_semestra()
    semestar = Semestar.objects.get(vrsta=podaci_tekuceg[0], skolska_godina_pocetak=podaci_tekuceg[1],
                                    skolska_godina_kraj=podaci_tekuceg[2])
    slusa_ponovac = Slusa_Ponovac.objects.filter(semestar=semestar, student=student)
    raspored = RasporedNastave.objects.get(semestar_id=semestar.id)
    for instanca in slusa_ponovac:
        for nastavnik in instanca.predmet.nastavnik_set.all():
            if nastavnik in instanca.nastavnici.all():
                termini = Termin.objects.filter(nastavnik=nastavnik, predmet=instanca.predmet, raspored=raspored)
                predmeti.extend(termini)
    return predmeti


