# coding: utf8
from django.conf.urls import patterns, url, include

urlpatterns = patterns('locks.views',
    url(r'^$', 'index', name='index'),
)