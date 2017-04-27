#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.conf import settings
import pytz

local_tz = pytz.timezone(settings.TIME_ZONE)


#
# 从UTC转成本地datetime
#
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

