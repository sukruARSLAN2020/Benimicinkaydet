from django.conf.urls import url
from .views import views


app_name = "MyDatabase"

urlpatterns = [

    url(r'^index/$', Ders_index, name="index"),

    url(r'^create/$', Ders_create, name='create'),

    url(r'^(?P<slug>[\w-]+)/$', Ders_detail, name='detail'),

    url(r'^(?P<slug>[\w-]+)/update/$', Ders_update, name="update"),

    url(r'^(?P<slug>[\w-]+)/delete/$', Ders_delete, name='delete'),
]