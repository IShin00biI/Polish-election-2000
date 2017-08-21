from django.conf.urls import url

from . import views

app_name='main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'voivodeship/(?P<pk>[\w\-]+)$', views.voivodeship, name='voivodeship'),
    url(r'district/(?P<pk>\d+)$', views.district, name='district'),
    url(r'commune/(?P<pk>[\w\-]+)$', views.commune, name='commune'),
]
