from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .dingtalk import send


# 异步任务
@shared_task
def sen_dingtalk_message(message):
    send(message)