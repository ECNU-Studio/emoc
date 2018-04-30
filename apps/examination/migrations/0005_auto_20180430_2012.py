# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-30 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0004_auto_20180422_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeinfo',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='\u59d3\u540d'),
        ),
        migrations.AddField(
            model_name='takeinfo',
            name='num',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5b66\u53f7'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.TextField(verbose_name='\u9009\u9879'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='\u95ee\u9898'),
        ),
    ]
