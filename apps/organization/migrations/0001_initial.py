# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-27 10:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name=b'\xe5\x9f\x8e\xe5\xb8\x82')),
                ('desc', models.TextField(verbose_name=b'\xe5\x9f\x8e\xe5\xb8\x82\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u57ce\u5e02',
                'verbose_name_plural': '\u57ce\u5e02',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\xba\xe6\x9e\x84\xe5\x90\x8d\xe7\xa7\xb0')),
                ('category', models.CharField(choices=[(b'pxjg', b'\xe5\x9f\xb9\xe8\xae\xad\xe6\x9c\xba\xe6\x9e\x84'), (b'gr', b'\xe4\xb8\xaa\xe4\xba\xba'), (b'gx', b'\xe9\xab\x98\xe6\xa0\xa1')], default=b'pxjg', max_length=20, verbose_name=b'\xe6\x9c\xba\xe6\x9e\x84\xe7\xb1\xbb\xe5\x88\xab')),
                ('desc', models.TextField(verbose_name=b'\xe6\x9c\xba\xe6\x9e\x84\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('tag', models.CharField(default=b'\xe5\x85\xa8\xe5\x9b\xbd\xe7\x9f\xa5\xe5\x90\x8d', max_length=10, verbose_name=b'\xe6\x9c\xba\xe6\x9e\x84\xe6\xa0\x87\xe7\xad\xbe')),
                ('click_nums', models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe5\x87\xbb\xe6\x95\xb0')),
                ('fav_nums', models.IntegerField(default=0, verbose_name=b'\xe6\x94\xb6\xe8\x97\x8f\xe6\x95\xb0')),
                ('image', models.ImageField(default=b'', upload_to=b'org/%Y/%m', verbose_name=b'\xe5\xb0\x81\xe9\x9d\xa2\xe5\x9b\xbe')),
                ('address', models.CharField(max_length=150, verbose_name=b'\xe6\x9c\xba\xe6\x9e\x84\xe5\x9c\xb0\xe5\x9d\x80')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('students', models.IntegerField(default=0, verbose_name=b'\xe5\xad\xa6\xe4\xb9\xa0\xe4\xba\xba\xe6\x95\xb0')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CityDict', verbose_name=b'\xe6\x89\x80\xe5\x9c\xa8\xe5\x9f\x8e\xe5\xb8\x82')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u673a\u6784',
                'verbose_name_plural': '\u8bfe\u7a0b\u673a\u6784',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe6\x95\x99\xe5\xb8\x88\xe5\x90\x8d\xe5\xad\x97')),
                ('work_years', models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xa5\xe4\xbd\x9c\xe5\xb9\xb4\xe9\x99\x90')),
                ('work_company', models.CharField(max_length=50, verbose_name=b'\xe5\xb0\xb1\xe8\x81\x8c\xe5\x85\xac\xe5\x8f\xb8')),
                ('work_position', models.CharField(max_length=50, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe8\x81\x8c\xe4\xbd\x8d')),
                ('points', models.CharField(max_length=50, verbose_name=b'\xe6\x95\x99\xe5\xad\xa6\xe7\x89\xb9\xe7\x82\xb9')),
                ('click_nums', models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe5\x87\xbb\xe6\x95\xb0')),
                ('fav_nums', models.IntegerField(default=0, verbose_name=b'\xe6\x94\xb6\xe8\x97\x8f\xe6\x95\xb0')),
                ('age', models.IntegerField(default=30, verbose_name=b'\xe5\xb9\xb4\xe9\xbe\x84')),
                ('image', models.ImageField(default=b'', upload_to=b'teacher/%Y/%m', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\x9c\xba\xe6\x9e\x84')),
            ],
            options={
                'verbose_name': '\u6559\u5e08',
                'verbose_name_plural': '\u6559\u5e08',
            },
        ),
    ]
