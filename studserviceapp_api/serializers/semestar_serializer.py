from rest_framework import serializers
from studserviceapp.models import Semestar


class SemestarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestar
        fields = '__all__'