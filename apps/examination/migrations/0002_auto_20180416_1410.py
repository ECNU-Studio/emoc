# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-16 14:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseold',
            options={'managed': False, 'verbose_name': '课程试题库', 'verbose_name_plural': '课程试题库'},
        ),
        migrations.AlterModelOptions(
            name='examination',
            options={'verbose_name': '课程试题', 'verbose_name_plural': '课程试题'},
        ),
        migrations.RemoveField(
            model_name='examination',
            name='name',
        ),
        migrations.AddField(
            model_name='examination',
            name='course',
            field=models.ForeignKey(default=datetime.datetime(2018, 4, 16, 14, 10, 41, 886425), on_delete=django.db.models.deletion.CASCADE, to='examination.CourseOld', verbose_name='试卷'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examination',
            name='question_nums',
            field=models.IntegerField(default=0, verbose_name='试题数'),
        ),
        migrations.AddField(
            model_name='examination',
            name='type',
            field=models.CharField(choices=[('fixed', '固定'), ('random', '随机')], default=datetime.datetime(2018, 4, 16, 14, 10, 45, 573319), max_length=32, verbose_name='类型'),
            preserve_default=False,
        ),
    ]
