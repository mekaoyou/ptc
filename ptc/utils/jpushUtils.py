#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
import jpush


def pushRecords(msg, tag, to_alias):
    """
    :param msg: push msg
    :param tag: push tag
    :param to_alias: push to who
    :return: 
    """
    _jpush = jpush.JPush(settings.JPUSH_APP_KEY, settings.JPUSH_MASTER_SECRET)
    _jpush.set_logging("DEBUG")
    push = _jpush.create_push()
    alias = [to_alias, ]
    alias1 = {"alias": alias}
    print alias1
    push.audience = jpush.audience(
        jpush.tag(tag, ),
        alias1
    )

    push.notification = jpush.notification(alert=msg)
    push.platform = jpush.all_
    print (push.payload)
    push.send()

