from django.urls import path, re_path
from .views import frontend
urlpatterns = [
    re_path(r'^(?:.*)/?$', frontend.index),
]