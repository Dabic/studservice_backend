from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from studserviceapp.korisne_funkcije import vrati_trenutni_semestar
from studserviceapp.models import Student, Grupa
from studserviceapp_api.serializers.grupa_serializer import GrupaSerializer
from studserviceapp_api.serializers.student_serializer import StudentSerializer
from django.shortcuts import HttpResponse


@api_view(['GET'])
def getAllStudenti(request):
    studenti = Student.objects.all()
    json = JSONRenderer().render(StudentSerializer(studenti, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
def getStudentiGrupa(request, grupa):
    grupa = Grupa.objects.get(oznaka_grupe=grupa)
    student_grupa = Student.grupa.through.objects.filter(grupa_id=grupa.id)
    studenti = []
    for sg in student_grupa:
        studenti.append(Student.objects.get(id=sg.student_id))
    json = JSONRenderer().render(StudentSerializer(studenti, many=True).data)
    return HttpResponse(json)


@api_view(['GET'])
def getStudentiGodina(request, godina):
    grupe = Grupa.objects.filter(oznaka_grupe__startswith=godina, semestar=vrati_trenutni_semestar())
    student_grupa = []
    for gr in grupe:
        student_grupa.extend(Student.grupa.through.objects.filter(grupa_id=gr.id))
    studenti = []
    print(student_grupa)
    for sg in student_grupa:
        studenti.append(Student.objects.get(id=sg.student_id))
    json = JSONRenderer().render(StudentSerializer(studenti, many=True).data)
    return HttpResponse(json)
