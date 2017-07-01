# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.StudentRegistrationView.as_view(), name='student_registration'),
]