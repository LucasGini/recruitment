# Generated by Django 3.1 on 2022-07-16 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20220713_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 16, 21, 58, 6, 624646), verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='job',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 16, 21, 58, 6, 624665), verbose_name='修改时间'),
        ),
    ]