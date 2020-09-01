from django.urls import re_path, path
from . import views

app_name = 'smzdm'
urlpatterns = [
    path('', views.index),
    re_path('(?P<id>[0-9]{8}).html', views.good_info, name='good_info')
]