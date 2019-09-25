from rest_framework import serializers
from studserviceapp.models import Student, Grupa
from studserviceapp_api.serializers.grupa_serializer import GrupaSerializer
from studserviceapp.korisne_funkcije import vratiTrenutnuGrupuZaStudenta

class StudentSerializer(serializers.ModelSerializer):
    grupa = serializers.SerializerMethodField()

    def get_grupa(self, obj):
        return GrupaSerializer(vratiTrenutnuGrupuZaStudenta(obj)).data

    class Meta:
        model = Student
        fields = ('ime', 'prezime', 'broj_indeksa', 'godina_upisa', 'smer', 'icon', 'grupa')