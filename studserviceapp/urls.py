from django.urls import re_path
from studserviceapp.views.frontend import frontend

urlpatterns = [
    re_path(r'^(?:.*)/?$', frontend.index),
]