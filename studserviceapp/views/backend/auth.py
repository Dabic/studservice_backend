from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import HttpResponse
from rest_framework import status
from studserviceapp.models import Student, Nalog, Nastavnik
from studserviceapp_api.serializers.nalog_serializer import NalogSerializer
from studserviceapp_api.serializers.student_serializer import StudentSerializer
from studserviceapp_api.serializers.nastavnik_serializer import NastavnikSerializer
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import requests
import json as jsn


@api_view(['POST'])
def authorize(request):
    response = JSONParser().parse(io.BytesIO(requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+request.data['token']).content))
    username = response['email'].split('@')[0]
    print(response)
    try:
        nalog = Nalog.objects.get(username=username)
    except Nalog.DoesNotExist:
        return HttpResponse({'error': 'Niste autoratizovani'}, status.HTTP_401_UNAUTHORIZED)

    if nalog.uloga == 'Administrator':
        nalogSerialized = NalogSerializer(nalog).data
        adminSerialized = {
            "ime": response['given_name'],
            "prezime": response['family_name']
        }
        json = JSONRenderer().render({'nalog': nalogSerialized, 'user': adminSerialized,
                                      'token': request.data['token'], 'authenticatedAs': 'Administrator'})
        return HttpResponse(json)
    elif nalog.uloga == 'student':
        student = Student.objects.get(nalog_id=nalog.id)
        student.icon = response['picture']
        student.save()
        nalogSerialized = NalogSerializer(nalog).data
        studentSerialized = StudentSerializer(student).data
        json = JSONRenderer().render({'nalog': nalogSerialized, 'user': studentSerialized,
                                      'token': request.data['token'], 'authenticatedAs': 'Student'})
        return HttpResponse(json)
    elif nalog.uloga == 'Nastavnik':
        nastavnik = Nastavnik.objects.get(nalog_id=nalog.id)
        nastavnikSerialized = NastavnikSerializer(nastavnik).data
        nalogSerialized = NalogSerializer(nalog).data
        json = JSONRenderer().render({'nalog': nalogSerialized, 'user': nastavnikSerialized,
                                      'token': request.data['token'], 'authenticatedAs': 'Nastavnik'})
        return HttpResponse(json)
    elif nalog.uloga == 'Sekretar':
        sekretarSerialized = {
            "ime": response['given_name'],
            "prezime": response['family_name']
        }
        nalogSerialized = NalogSerializer(nalog).data
        json = JSONRenderer().render({'nalog': nalogSerialized, 'user': sekretarSerialized,
                                      'token': request.data['token'], 'authenticatedAs': 'Sekretar'})
        return HttpResponse(json)
