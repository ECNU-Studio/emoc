# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-21 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacheres', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursestoTeachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Courses', verbose_name='\u8bfe\u7a0b')),
                ('teacheres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacheres.Teacheres', verbose_name='\u57f9\u8bad\u5e08')),
            ],
        ),
    ]