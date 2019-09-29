from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from studserviceapp.models import Student, Grupa
from studserviceapp_api.serializers.grupa_serializer import GrupaSerializer
from studserviceapp_api.serializers.student_serializer import StudentSerializer
from django.shortcuts import HttpResponse


@api_view(['GET'])
def getAllStudenti(request, tip):
    if tip == 'svi':
        studenti = Student.objects.all()
        json = JSONRenderer().render(StudentSerializer(studenti, many=True).data)
        return HttpResponse(json)
