# coding: utf-8
__author__ = "HanQian"

from django import forms
from courese.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)