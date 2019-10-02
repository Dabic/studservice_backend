from rest_framework import serializers
from studserviceapp.models import Grupa
from .semestar_serializer import SemestarSerializer
from studserviceapp.korisne_funkcije import broj_studenata_grupe


class GrupaSerializer(serializers.ModelSerializer):
    semestar = SemestarSerializer
    broj_studenata = serializers.SerializerMethodField()

    def get_broj_studenata(self, obj):
        return broj_studenata_grupe(obj)

    class Meta:
        model = Grupa
        fields = '__all__'
