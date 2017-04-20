#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms


class RegForm(forms.Form):
    roleId = forms.IntegerField()
    classId = forms.IntegerField(required=False)
    userName = forms.CharField(max_length=16)
    pwd = forms.CharField(max_length=16)
    phone = forms.CharField(max_length=16, required=False)
    email = forms.EmailField(max_length=50, required=False)


class LoginForm(forms.Form):
    userName = forms.CharField(max_length=16)
    pwd = forms.CharField(max_length=16)


class RecordForm(forms.Form):
    lessonId = forms.IntegerField()
    wifi = forms.CharField(max_length=16)


class ResetForm(forms.Form):
    userName = forms.CharField(max_length=16)


class LessonForm(forms.Form):
    type = forms.IntegerField(max_value=1, required=False)


class RecordsForm(forms.Form):
    lessonId = forms.IntegerField()
