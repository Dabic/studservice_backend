from rest_framework.renderers import JSONRenderer
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from studserviceapp.models import Nalog
from studserviceapp_api.serializers.nalog_serializer import NalogSerializer
from studserviceapp_api.permissions import permissions


@api_view(['POST'])
@permission_classes([permissions.AdminPermission | permissions.SekretarPermission | permissions.NastavnikPermission])
def get_all_nalozi(request):
    nalozi = Nalog.objects.all()
    json = JSONRenderer().render(NalogSerializer(nalozi, many=True).data)
    return HttpResponse(json)
