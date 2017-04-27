#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery import task
from models import *
import datetime
from django.utils.timezone import utc
from views import getRecordsData
from utils import jpushUtils


@task
def test():
    print u'++++++++++I am running now ++++++++++++'


@task
def checkLessonRecords():
    lessons = PTCLesson.objects.filter(pushed=False, startTime__lt=datetime.datetime.utcnow().replace(tzinfo=utc))
    print len(lessons)
    for lesson in lessons:
        # get records
        recordsData = getRecordsData(lesson, lesson.teacher)
        """{
            u'total': len(studens),
            u'records': len(recordsTotal),
            u'valid': len(validRecords),
            u'late': len(lateRecords),
            u'lost': loseRecords,
        }"""
        # push msg
        # msg = {u'lesson': lesson, u'records': recordsData}
        msg = u'%s老师，%s 《%s》课程学生考勤结果统计如下：应到%s人，打卡%s人，有效打卡%s人，迟到%s人，旷课%s。' % \
              (lesson.teacher.name, lesson.startTime, lesson.name, recordsData[u'total'], recordsData[u'records'],
               recordsData[u'valid'], recordsData[u'late'], recordsData[u'lost'])
        jpushUtils.pushRecords(msg, lesson.teacher.role.id, lesson.teacher.id)
        # update lesson
        lesson.pushed = True
        lesson.save()


