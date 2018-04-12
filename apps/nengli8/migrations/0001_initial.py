# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-12 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='companys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='\u540d\u79f0')),
                ('account', models.CharField(max_length=45, verbose_name='\u8d26\u6237')),
                ('password', models.CharField(max_length=45, verbose_name='\u5bc6\u7801')),
                ('email', models.CharField(max_length=45, verbose_name='\u90ae\u7bb1')),
                ('legalperson', models.CharField(max_length=45, verbose_name='\u6cd5\u4eba')),
                ('address', models.CharField(max_length=45, verbose_name='\u4f01\u4e1a\u5730\u5740')),
                ('cover', models.CharField(max_length=45, verbose_name='\u4f01\u4e1a\u5c01\u9762')),
                ('memo', models.CharField(max_length=45, verbose_name='\u5907\u6ce8')),
                ('state', models.CharField(max_length=45, verbose_name='\u662f\u5426\u6709\u6548')),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a',
                'verbose_name_plural': '\u4f01\u4e1a',
                'permissions': (('export', 'Can export questionnaire answers'), ('management', 'Management Tools')),
            },
        ),
    ]
