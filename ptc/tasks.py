#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery import task
from models import *
import datetime
from django.utils.timezone import utc
from views import getRecordsData
from utils import jpushUtils, jsonUtils


@task
def test():
    print u'++++++++++I am running now ++++++++++++'


@task
def checkLessonRecords():
    lessons = PTCLesson.objects.all()
    print len(lessons)
    nowTime = datetime.datetime.utcnow().replace(tzinfo=utc)
    for lesson in lessons:
        if nowTime > lesson.startTime:
            # get records
            recordsData = getRecordsData(lesson, lesson.teacher)
            # push msg
            msg = {u'lesson': lesson, u'records': recordsData}
            jpushUtils.pushRecords(jsonUtils.getJson(msg), lesson.teacher.role.id, lesson.teacher.id)
            # update lesson
            lesson.pushed = True
            lesson.save()


