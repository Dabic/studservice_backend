from rest_framework import serializers
from studserviceapp.models import Predmet

class PredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predmet
        fields = ('naziv', )