from django.db import models


VRSTA_SEMESTRA_CHOICES = (
    ('parni', 'parni'),
    ('neparni', 'neparni'),
)

class Semestar(models.Model):
    vrsta = models.CharField(max_length=20, choices=VRSTA_SEMESTRA_CHOICES)  # parni/neparni
    skolska_godina_pocetak = models.IntegerField()  # primer 2018
    skolska_godina_kraj = models.IntegerField()  # primer 2019
    aktivan = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "semestri"

    def __str__(self):
        return self.vrsta + " " + str(self.skolska_godina_pocetak) + "/" + str(self.skolska_godina_kraj)


class Grupa(models.Model):
    oznaka_grupe = models.CharField(max_length=10)
    smer = models.CharField(max_length=20, null=True)
    semestar = models.ForeignKey(Semestar, on_delete=models.DO_NOTHING)  # BILO JE NOTHING

    class Meta:
        verbose_name_plural = "grupe"

    def __str__(self):
        return self.oznaka_grupe


class Nalog(models.Model):
    username = models.CharField(max_length=200)
    lozinka = models.CharField(max_length=100, null=True)  # google login, necemo koristiti password
    uloga = models.CharField(max_length=50)  # student, nastavnik, sekretar, administrator

    class Meta:
        verbose_name_plural = "nalozi"

    def __str__(self):
        return self.username + " " + self.uloga


class Student(models.Model):
    ime = models.CharField(max_length=200)
    prezime = models.CharField(max_length=200)
    broj_indeksa = models.IntegerField()
    godina_upisa = models.IntegerField()
    smer = models.CharField(max_length=20)
    nalog = models.ForeignKey(Nalog, on_delete=models.CASCADE)  # BILO JE CASCADE
    grupa = models.ManyToManyField(Grupa)
    icon = models.ImageField(upload_to='media', default='no-image.gif')

    class Meta:
        verbose_name_plural = "studenti"

    def __str__(self):
        return self.ime + " " + self.prezime + " " + self.smer + " " + str(self.broj_indeksa) + "/" + str(
            self.godina_upisa)


class Predmet(models.Model):
    naziv = models.CharField(max_length=200)
    espb = models.IntegerField(null=True)
    semestar_po_programu = models.IntegerField(null=True)  # redni broj semestra u kom se slusa predmet
    fond_predavanja = models.IntegerField(null=True)
    fond_vezbe = models.IntegerField(null=True)
    sifra = models.CharField(max_length=15, default='0')
    izborni = models.BooleanField(default=False)  # ?? izborni na jednom smeru, a na drugom ne
    opis = models.TextField(null=True)
    opis_fajl = models.FileField(upload_to='opispredmeta/',null=True)

    class Meta:
        verbose_name_plural = "predmeti"

    def __str__(self):
        return self.naziv


class Nastavnik(models.Model):
    ime = models.CharField(max_length=200)
    prezime = models.CharField(max_length=200)
    titula = models.CharField(max_length=20, null=True)
    zvanje = models.CharField(max_length=40, null=True)
    nalog = models.ForeignKey(Nalog, on_delete=models.CASCADE)  # BILO JE CASCADE
    predmet = models.ManyToManyField(Predmet)

    class Meta:
        verbose_name_plural = "nastavnici"

    def __str__(self):#ne menjati ovaj toString
        return self.ime + " " + self.prezime

# student slusa neki predmet u nekom semestru kod odredjenih nastavnika (profesora, asistenta, kao ponovac)
class Slusa_Ponovac(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semestar = models.ForeignKey(Semestar, on_delete=models.DO_NOTHING)
    predmet = models.ForeignKey(Predmet, on_delete=models.DO_NOTHING)
    nastavnici = models.ManyToManyField(Nastavnik)

    class Meta:
        verbose_name_plural = "ponovci"


class RasporedNastave(models.Model):
    datum_unosa = models.DateTimeField()
    semestar = models.ForeignKey(Semestar, on_delete=models.PROTECT)  # BILO JE PROTECT

    class Meta:
        verbose_name_plural = "rasporedi nastave"


class Termin(models.Model):
    oznaka_ucionice = models.CharField(max_length=50)
    pocetak = models.TimeField()
    zavrsetak = models.TimeField()
    dan = models.CharField(max_length=15)
    tip_nastave = models.CharField(max_length=15)  # predavanja, vezbe, praktikum
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.DO_NOTHING)  # BILO JE NOTHING
    predmet = models.ForeignKey(Predmet, on_delete=models.DO_NOTHING)  # BILO JE NOTHING
    grupe = models.ManyToManyField(Grupa)
    raspored = models.ForeignKey(RasporedNastave, on_delete=models.CASCADE)  # BILO JE CASCADE

    @property
    def naziv_predmeta(self):
        return self.predmet.naziv

    @property
    def ime_prezime_nastavnika(self):
        return self.nastavnik.ime + ' ' + self.nastavnik.prezime

    @property
    def oznaka_grupe(self):
        return self.grupe.oznaka_grupe

    class Meta:
        verbose_name_plural = "termini"

    def __str__(self):
        return self.oznaka_ucionice + " " + str(self.pocetak) + " " + str(
            self.zavrsetak) + " " + self.dan + " " + self.tip_nastave + " " + str(
            self.nastavnik) + " " + self.predmet.naziv


class IzbornaGrupa(models.Model):
    oznaka_grupe = models.CharField(max_length=20)
    oznaka_semestra = models.IntegerField()
    kapacitet = models.IntegerField()
    smer = models.CharField(max_length=20)
    aktivna = models.BooleanField()
    za_semestar = models.ForeignKey(Semestar, on_delete=models.DO_NOTHING)
    predmeti = models.ManyToManyField(Predmet)

    class Meta:
        verbose_name_plural = "Izborne grupe"

    def __str__(self):
        return self.oznaka_grupe + " " + str(self.oznaka_semestra) + " " + str(self.kapacitet) + " " + self.smer + " " + str(
            self.aktivna)


class IzborGrupe(models.Model):
    ostvarenoESPB = models.IntegerField()
    upisujeESPB = models.IntegerField()
    broj_polozenih_ispita = models.IntegerField()
    upisuje_semestar = models.IntegerField()  # redni broj semestra
    prvi_put_upisuje_semestar = models.BooleanField()
    nacin_placanja = models.CharField(max_length=30)
    nepolozeni_predmeti = models.ManyToManyField(Predmet)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    izabrana_grupa = models.ForeignKey(IzbornaGrupa, on_delete=models.CASCADE)
    upisan = models.BooleanField()  # na pocetku staviti false

    class Meta:
        verbose_name_plural = "Izbori grupa"


class VazniDatumi(models.Model):
    kategorija = models.CharField(
        max_length=200)  # kolokvijumske nedelje, ispitni rokovi, placanje skolarine na rate,...
    oznaka = models.CharField(max_length=200)  # I, Jan, Feb. I  rata, RAF Hackaton,...
    datum_od = models.DateField(null=True)
    datum_do = models.DateField(null=True)
    okvirno = models.CharField(max_length=200, null=True)
    skolska_godina = models.CharField(max_length=15)  # 2018/2019

    def _str_(self):
        return self.kategorija+" "+self.oznaka+" "+self.datum_od.str+"-"+self.datum_do.str

    class Meta:
        verbose_name_plural = "vazni datumi"


class Konsultacije(models.Model):
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE, null=True)
    mesto = models.CharField(max_length=50)
    vreme_od = models.TimeField()
    vreme_do = models.TimeField()
    dan = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "konsultacije"


class Obavestenje(models.Model):
    postavio = models.ForeignKey(Nalog, on_delete=models.DO_NOTHING)
    naslov = models.CharField(max_length=100)
    datum_postavljanja = models.DateTimeField()
    tekst = models.CharField(max_length=1000)
    fajl = models.FileField(upload_to='obavestenja/')

    class Meta:
        verbose_name_plural = "obavestenja"


class RasporedPolaganja(models.Model):
    vazan_datum = models.ForeignKey(VazniDatumi,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "rasporedi polaganja"


class TerminPolaganja(models.Model):
    ucionice = models.CharField(max_length=100)
    pocetak = models.TimeField()
    zavrsetak = models.TimeField()
    datum = models.DateField()
    dan = models.CharField(max_length=100)
    raspored_polaganja = models.ForeignKey(RasporedPolaganja, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.DO_NOTHING)
    nastavnik = models.ForeignKey(Nastavnik, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "termini polaganja"
