#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

# Register your models here.


class PTCClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)
    list_display_links = ('id', 'name', )
    ordering = ('id', )
    list_per_page = 30


class PTCClassRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'wifi', 'position',)
    search_fields = ('name',)
    list_display_links = ('id', 'name', )
    ordering = ('id', )
    list_per_page = 30


class PTCRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_display_links = ('id', 'name', )
    ordering = ('id', )
    list_per_page = 30


class PTCUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'tel', 'pClass', )
    search_fields = ('name',)
    list_display_links = ('id', 'name', )
    ordering = ('id', )
    list_per_page = 30


class PTCLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pClass', 'teacher', 'pClassRoom', 'startTime', 'endTime',)
    search_fields = ('name',)
    list_display_links = ('id', 'name', )
    ordering = ('id', )
    list_per_page = 30

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = PTCUser.objects.filter(role=PTCRole.objects.get(name=u'老师'))
            return super(PTCLessonAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PTCRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'recordTime', 'recordUser', 'recordLesson', 'recordWifi', )
    search_fields = ('recordUser',)
    list_display_links = ('id', 'recordUser', )
    ordering = ('id', )
    list_per_page = 30


class PTCResetPWDApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'applyUser', 'applyTime', 'resetState', )
    search_fields = ('applyUser',)
    list_display_links = ('id', 'applyUser', )
    ordering = ('id', )
    list_per_page = 30


admin.site.register(PTCClass, PTCClassAdmin)
admin.site.register(PTCClassRoom, PTCClassRoomAdmin)
admin.site.register(PTCRole, PTCRoleAdmin)
admin.site.register(PTCUser, PTCUserAdmin)
admin.site.register(PTCLesson, PTCLessonAdmin)
admin.site.register(PTCRecord, PTCRecordAdmin)
admin.site.register(PTCResetPWDApply, PTCResetPWDApplyAdmin)

