# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-10 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20180410_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
