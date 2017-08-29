from django.conf.urls import url

from . import views

app_name='main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^country/Polska', views.index, name='Polska'),
    url(r'^login/$', views.login_view, name='login', kwargs={'username': ''}),
    url(r'^search/$', views.search_view, name='search'),
    url(r'voivodeship/(?P<pk>[\w\-]+)$', views.voivodeship, name='voivodeship'),
    url(r'district/(?P<pk>\d+)$', views.district, name='district'),
    url(r'commune/(?P<pk>[\w\-]+)$', views.commune, name='commune'),
]
