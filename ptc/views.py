#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.db.models.query import QuerySet
from models import *
from forms import *
from django.views.decorators.csrf import csrf_exempt
from utils import const, jsonUtils
import datetime

# Create your views here.
const.FRONT_USER = u'front_user'


@csrf_exempt
def index(request):
    return render(request, 'ptc_test.html')


@csrf_exempt
def getClass(request):
    classes = PTCClass.objects.all()
    result = {u'data': classes, u'success': True}
    json = jsonUtils.getJson(result)
    return HttpResponse(json[1:-1], content_type="application/json")
    #return toJSON(classes, True if len(classes) > 0 else False)


def getRoles(request):
    roles = PTCRole.objects.all()
    result = {u'data': roles, u'success': True}
    json = jsonUtils.getJson(result)
    return HttpResponse(json[1:-1], content_type="application/json")
    #return toJSON(roles, True if len(roles) > 0 else False)


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
    elif roles[0].name == u'老师':
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
    users = PTCUser.objects.filter(name=logData['userName'], pwd=logData['pwd'])
    if len(users) <= 0:
        return toJSON(u'用户名密码错误', False)
    request.session[const.FRONT_USER] = users[0].id
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
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    userId = request.session.get(const.FRONT_USER, None)
    if userId is None:
        return toJSON(u'用户未登陆', False)
    form = LessonForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)
    loginUser = PTCUser.objects.get(id=userId)
    if loginUser.role.name == u'学生':
        lessons = PTCLesson.objects.filter(pClass=loginUser.pClass, endTime__gt=datetime.datetime.now()).order_by(
            "endTime")
    else:
        type = int(form.cleaned_data['type'] if form.cleaned_data['type'] is not None else 0)
        if type == 0:
            lessons = PTCLesson.objects.filter(teacher=loginUser, endTime__gt=datetime.datetime.now()).order_by(
                "endTime")
        elif type == 1:
            lessons = PTCLesson.objects.filter(teacher=loginUser, endTime__lt=datetime.datetime.now()).order_by(
                "endTime")
    return toJSON(lessons, True)


@csrf_exempt
def tick(request):
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
    if loginUser.role.name == u'学生':
        if lessons[0].pClass != loginUser.PClass:
            return toJSON(u'无权打卡', False)
    else:
        if lessons[0].teacher != loginUser:
            return toJSON(u'无权打卡')
    records = PTCRecord.objects.filter(recordLesson=lessons[0], recordUser=loginUser)
    if len(records) > 0:
        return toJSON(u'已打卡', False)
    PTCRecord.objects.create(recordLesson=lessons[0], recordUser=loginUser, recordTime=datetime.datetime.now(),
                             recordWifi=recData['wifi'])
    return toJSON(u'打卡成功', True)


@csrf_exempt
def resetPwd(request):
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    form = ResetForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)
    users = PTCUser.objects.filter(name=form.cleaned_data['userName'])
    if len(users) <= 0:
        return toJSON(u'用户不存在', False)
    PTCResetPWDApply.objects.get_or_create(applyUser=users[0], resetState=False)
    return toJSON(u'申请成功', True)


@csrf_exempt
def getRecords(request):
    if request.method != 'POST':
        return toJSON(u'请求不合法', False)
    userId = request.session.get(const.FRONT_USER, None)
    if userId is None:
        return toJSON(u'用户未登陆', False)
    loginUser = PTCUser.objects.get(id=userId)
    if loginUser.role.name != u'老师':
        return toJSON(u'无权查看考勤记录', False)
    if userId is None:
        return toJSON(u'用户未登陆', False)
    form = RecordsForm(request.POST)
    if not form.is_valid():
        return toJSON(u'参数校验失败', False)
    lessonId = int(form.cleaned_data['lessonId'])
    lessons = PTCLesson.objects.filter(id=lessonId)
    if len(lessons) <= 0:
        return toJSON(u'课程不存在', False)
    if lessons[0].teacher != loginUser:
        return toJSON(u'无权查看考勤记录', False)
    studens = PTCUser.objects.filter(pClass=lessons[0].pClass)
    recordsTotal = PTCRecord.objects.filter(recordLesson=lessons[0],
                                            recordTime__lt=lessons[0].endTime,
                                            recordTime__gt=getValidTime(lessons[0].startTime)).exclude(recordUser=loginUser)
    validRecords = PTCRecord.objects.filter(recordLesson=lessons[0],
                                             recordWifi=lessons[0].pClassRoom.wifi,
                                            recordTime__lt=lessons[0].endTime,
                                            recordTime__gt=getValidTime(lessons[0].startTime)).exclude(recordUser=loginUser)
    lateRecords = PTCRecord.objects.filter(recordLesson=lessons[0],
                                             recordWifi=lessons[0].pClassRoom.wifi,
                                            recordTime__lt=lessons[0].endTime,
                                           recordTime__gt=lessons[0].startTime).exclude(recordUser=loginUser)
    loseRecords = len(studens) - len(validRecords)
    result = {
        u'total': len(studens),
        u'records': len(recordsTotal),
        u'valid': len(validRecords),
        u'late': len(lateRecords),
        u'lost': loseRecords,
    }
    return toJSON(result, True)


def toJSON(arr, success):
    if isinstance(arr, QuerySet):
        data = serializers.serialize("json", arr, use_natural_foreign_keys=True)
    else:
        data = arr
    result = {r'success': success, r'data': data}
    return JsonResponse(result, safe=False)


def getValidTime(startTime):
    tenMinAgo = datetime.timedelta(minutes=10)
    return startTime - tenMinAgo

