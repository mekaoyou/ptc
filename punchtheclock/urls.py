#!/usr/bin/python
# -*- coding: utf-8 -*-

"""punchtheclock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ptc import views

admin.site.site_header = u'考勤管理'
admin.site.site_title = u'考勤管理'

urlpatterns = [
    url(r'^$', views.index),
    url(r'^record/', views.getRecords),
    url(r'^reset/', views.resetPwd),
    url(r'^tick/', views.tick),
    url(r'^lesson/', views.getLesson),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^reg/', views.reg),
    url(r'^roles/', views.getRoles),
    url(r'^class/', views.getClass),
    url(r'^admin/', admin.site.urls),
]
