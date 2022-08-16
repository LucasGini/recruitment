from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('recruitment')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# 注意下面引用的tasks.add的方法，必须显示import，才能正确注册

from recruitment.tasks import add

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'recruitment.tasks,add',
        'schedule': 10.0,
        'args': (16, 4,)
    }
}

# 系统启动时自动注册定时日任务
from celery.schedules import crontab


@app.on_after_configure.connect # 系统启动完成后再去执行这个方法
def setup_periodic_tasks(sender, **kwargs):
    # 添加定时任务 每10秒运行一次
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')
    # 添加定时任务 每30秒运行一次
    sender.add_periodic_task(30.0, test.s('world'), expires=10)
    # 添加定时任务 每周一7点30分运行一次
    sender.add_periodic_task(
        crontab(hour=7, minute=20, day_of_week=1),  # crontab表达式
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)

# import json
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# # 创建定时策略
# schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
# # 再创建任务
# task = PeriodicTask.objects.create(interval=schedule, name='say welcome 3203843000', task='recruitment.celery.test', args=json.dumps(['welcome']))


app.conf.timezone = "Asia/Shanghai"