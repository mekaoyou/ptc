#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.db import models

# Create your models here.


class PTCClass(models.Model):
    name = models.CharField(verbose_name=u'班级名称', max_length=16, unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    # natual_key的序列化
    def natural_key(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'班级'
        verbose_name_plural = u'班级'


class PTCClassRoom(models.Model):
    name = models.CharField(verbose_name=u'教室名', max_length=16, unique=True)
    wifi = models.CharField(verbose_name=u'教室WIFI', max_length=16)
    position = models.CharField(verbose_name=u'教室位置坐标', blank=True, max_length=16)

    def __unicode__(self):
        return u'%s' % self.name

    # natual_key的序列化
    def natural_key(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'教室'
        verbose_name_plural = u'教室'


class PTCRole(models.Model):
    name = models.CharField(verbose_name=u'角色名', max_length=16, unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色'


class PTCUser(models.Model):
    role = models.ForeignKey(PTCRole, verbose_name=u'角色')
    pClass = models.ForeignKey(PTCClass, verbose_name=u'班级', blank=True, null=True)
    name = models.CharField(verbose_name=u'姓名', max_length=16, unique=True)
    pwd = models.CharField(verbose_name=u'密码', max_length=16,)
    tel = models.CharField(verbose_name=u'电话', max_length=11, blank=True, )
    email = models.EmailField(verbose_name=u'邮箱', max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    # natual_key的序列化
    def natural_key(self):
        return u'%s' % self.name

    def save(self,  *args, **kwargs):
        isupdate = self.id is not None
        super(PTCUser, self).save(*args, **kwargs)
        if isupdate and self.email is not None:
            print "++++++++++++ send email +++++++++", self.email
            send_mail(u'考勤系统密码已重置', u'新密码:%s' % self.pwd, settings.DEFAULT_FROM_EMAIL,
                      [self.email], fail_silently=False)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'


class PTCLesson(models.Model):
    name = models.CharField(verbose_name=u'课程名称', max_length=16, unique=True)
    pClass = models.ForeignKey(PTCClass, verbose_name=u'班级')
    teacher = models.ForeignKey(PTCUser, verbose_name=u'老师')
    pClassRoom = models.ForeignKey(PTCClassRoom, verbose_name=u'教室信息')
    startTime = models.DateTimeField(verbose_name=u'上课时间')
    endTime = models.DateTimeField(verbose_name=u'下课时间')
    pushed = models.BooleanField(verbose_name=u'打卡统计已推送', default=False)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'课程安排'
        verbose_name_plural = u'课程安排'


class PTCRecord(models.Model):
    recordTime = models.DateTimeField(verbose_name=u'打卡时间', auto_now=True)
    recordUser = models.ForeignKey(PTCUser, verbose_name=u'打卡人')
    recordLesson = models.ForeignKey(PTCLesson, verbose_name=u'课程安排')
    recordWifi = models.CharField(verbose_name=u'打卡WIFI', max_length=16)
    recordPosition = models.CharField(verbose_name=u'打卡坐标', max_length=16, blank=True)

    def __unicode__(self):
        return u'%s' % self.recordUser

    class Meta:
        verbose_name = u'打卡记录'
        verbose_name_plural = u'打卡记录'


class PTCResetPWDApply(models.Model):
    applyUser = models.ForeignKey(PTCUser, verbose_name=u'申请人')
    resetState = models.BooleanField(verbose_name=u'是否重置', default=False)
    applyTime = models.DateTimeField(verbose_name=u'申请时间', auto_now=True)

    def __unicode__(self):
        return u'%s' % self.applyUser

    class Meta:
        verbose_name = u'密码重置申请'
        verbose_name_plural = u'密码重置申请'

