#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.db.models.query import QuerySet
from models import *
from forms import *
from django.views.decorators.csrf import csrf_exempt
from utils import const
import datetime

# Create your views here.
const.FRONT_USER = u'front_user'


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


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    form = LoginForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)
    logData = form.cleaned_data
    user = PTCUser.objects.get(name=logData['userName'], pwd=logData['pwd'])
    if user is None:
        return toJSON(u'用户名密码错误', False)
    request.session[const.FRONT_USER] = user.id
    return toJSON(u'登陆成功', True)


@csrf_exempt
def logout(request):
    try:
        del request.session[const.FRONT_USER]
    except KeyError:
        pass
    return toJSON(u'登出成功', True)


@csrf_exempt
def getLesson(request):
    userId = request.session.get(const.FRONT_USER, None)
    if userId is None:
        return toJSON(u'用户未登陆', False)
    loginUser = PTCUser.objects.get(id=userId)
    if loginUser.role.name == u'学生':
        lessons = PTCLesson.objects.filter(pClass=loginUser.pClass, endTime__gt=datetime.datetime.now())
    else:
        lessons = PTCLesson.objects.filter(teacher=loginUser)
    return toJSON(lessons, True)


@csrf_exempt
def record(request):
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    userId = request.session.get(const.FRONT_USER, None)
    if userId is None:
        return toJSON(u'用户未登陆', False)
    form = RecordForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)
    recData = form.cleaned_data
    lessons = PTCLesson.objects.filter(id=recData['lessonId'], endTime__gt=datetime.datetime.now())
    if len(lessons) <= 0:
        return toJSON(u'无效打卡，课程不存在或已结束', False)
    loginUser = PTCUser.objects.get(id=userId)
    records = PTCRecord.objects.filter(recordLesson=lessons[0], recordUser=loginUser)
    if len(records) > 0:
        return toJSON(u'已打卡', False)
    PTCRecord.objects.create(recordLesson=lessons[0], recordUser=loginUser, recordTime=datetime.datetime.now(),
                             recordWifi=recData['wifi'])
    return toJSON(u'打卡成功', True)


def toJSON(arr, success):
    if isinstance(arr, QuerySet):
        data = serializers.serialize("json", arr, use_natural_foreign_keys=True)
    else:
        data = arr
    result = {r'success': success, r'data': data}
    return JsonResponse(result, safe=False)


