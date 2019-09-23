from rest_framework import serializers
from studserviceapp.models import IzbornaGrupa
from .semestar_serializer import SemestarSerializer
from .predmet_serializer import PredmetSerializer
from studserviceapp.korisne_funkcije import provera_kapaciteta_izborne_grupe
class IzbornaGrupaSerializer(serializers.ModelSerializer):
    za_semestar = SemestarSerializer()
    predmeti = PredmetSerializer(many=True)
    broj_studenata = serializers.SerializerMethodField()

    def get_broj_studenata(self, obj):
        return provera_kapaciteta_izborne_grupe(obj)

    class Meta:
        model = IzbornaGrupa
        fields = '__all__'