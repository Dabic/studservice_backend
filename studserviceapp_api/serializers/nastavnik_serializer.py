from rest_framework import serializers
from studserviceapp.models import Nastavnik

class NastavnikSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nastavnik
        fields = ('ime', 'prezime', 'titula', 'zvanje')