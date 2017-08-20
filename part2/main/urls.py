from django.conf.urls import url

from . import views

app_name='main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'voivodeships/(?P<pk>\w+)$', views.voivodeship, name='voivodeship'),
    url(r'districts/(?P<pk>\d+)$', views.district, name='district'),
    url(r'communes/(?P<pk>\w+)$', views.commune, name='commune'),
]
