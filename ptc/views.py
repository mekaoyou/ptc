#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.db.models.query import QuerySet
from models import *
from forms import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def index(request):
    return render(request, 'ptc_test.html')


@csrf_exempt
def getClass(request):
    classes = PTCClass.objects.all()
    return toJSON(classes, True if len(classes) > 0 else False)


@csrf_exempt
def getRoles(request):
    roles = PTCRole.objects.all()
    return toJSON(roles, True if len(roles) > 0 else False)


@csrf_exempt
def reg(request):
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    form = RegForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)

    regData = form.cleaned_data
    if len(PTCUser.objects.filter(name=regData['userName'])) > 0:
        return toJSON(u'用户已存在', False)

    roles = PTCRole.objects.filter(id=regData['roleId'], )
    if len(roles) <= 0:
        return toJSON(u'角色不存在', False)

    if regData['classId'] is not None and roles[0].name == u'学生':
        classes = PTCClass.objects.filter(id=regData['classId'],)
        if len(classes) <= 0:
            return toJSON(u'班级不存在', False)

        PTCUser.objects.get_or_create(role=roles[0], pClass=classes[0], name=regData['userName'],
                                      pwd=regData['pwd'], tel=regData['phone'])
    elif roles[0].name is u'老师':
        PTCUser.objects.get_or_create(role=roles[0], name=regData['userName'], pwd=regData['pwd'], tel=regData['phone'])
    else:
        return toJSON(u'注册失败', False)

    return toJSON(u'注册成功', True)


def toJSON(arr, success):
    if isinstance(arr, QuerySet):
        data = serializers.serialize("json", arr, use_natural_foreign_keys=True)
    else:
        data = arr
    result = {r'success': success, r'data': data}
    return JsonResponse(result, safe=False)


