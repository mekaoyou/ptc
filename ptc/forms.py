#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms


class RegForm(forms.Form):
    roleId = forms.IntegerField()
    classId = forms.IntegerField(required=False)
    userName = forms.CharField(max_length=16)
    pwd = forms.CharField(max_length=16)
    phone = forms.CharField(max_length=16, required=False)



