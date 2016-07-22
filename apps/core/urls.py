from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from apps.core import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),

    url(r'^solve/$', views.solve),
    url(r'^solve/(\d)+/$', views.solve),
]
