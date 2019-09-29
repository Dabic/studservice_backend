from rest_framework import serializers
from studserviceapp.models import Nalog

class NalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nalog
        fields = '__all__'
