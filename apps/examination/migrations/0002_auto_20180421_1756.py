# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-21 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takeinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nengli8.UserOld', verbose_name='\u95ee\u5377\u7528\u6237'),
        ),
    ]
