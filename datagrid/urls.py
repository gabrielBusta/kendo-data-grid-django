from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^employees/', views.employees, name='employees'),
    url(r'^titles/', views.titles, name='titles'),
    url(r'^cities/', views.cities, name='cities'),
]
