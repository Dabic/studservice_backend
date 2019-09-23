from rest_framework import serializers
from studserviceapp.models import Grupa
from .semestar_serializer import SemestarSerializer

class GrupaSerializer(serializers.ModelSerializer):
    semestar = SemestarSerializer
    class Meta:
        model = Grupa
        fields = '__all__'