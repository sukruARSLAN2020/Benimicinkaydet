from django.conf.urls import url
from .views import *

app_name = "MyDatabase"

urlpatterns = [

    url(r'^index/$', MyDatabase_index, name="index"),

    url(r'^create/$', MyDatabase_create, name='create'),

    url(r'^(?P<slug>[\w-]+)/$', MyDatabase_detail, name='detail'),

    url(r'^(?P<slug>[\w-]+)/update/$', MyDatabase_update, name="update"),

    url(r'^(?P<slug>[\w-]+)/delete/$', MyDatabase_delete, name='delete'),
]