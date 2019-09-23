from rest_framework import serializers
from studserviceapp.models import Termin
from .grupa_serializer import GrupaSerializer


class TerminSerializer(serializers.ModelSerializer):
    naziv_predmeta = serializers.ReadOnlyField()
    ime_prezime_nastavnika = serializers.ReadOnlyField()
    grupe = GrupaSerializer(many=True)
    class Meta:
        model = Termin
        fields = ('id', 'naziv_predmeta', 'ime_prezime_nastavnika', 'grupe','oznaka_ucionice', 'dan', 'pocetak', 'zavrsetak', 'tip_nastave')