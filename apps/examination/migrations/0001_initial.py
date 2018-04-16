# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-16 22:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOld',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=52, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\x90\x8d\xe5\xad\x97')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u8bd5\u9898\u5e93',
                'db_table': 'courses',
                'managed': False,
                'verbose_name_plural': '\u8bfe\u7a0b\u8bd5\u9898\u5e93',
            },
        ),
        migrations.CreateModel(
            name='ExaminationStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examination', models.IntegerField()),
                ('name', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('question', models.IntegerField()),
                ('question_text', models.CharField(max_length=128, verbose_name='\u95ee\u9898')),
                ('qsort', models.IntegerField()),
                ('type', models.CharField(max_length=32)),
                ('choice', models.IntegerField()),
                ('choice_text', models.CharField(max_length=128, verbose_name='\u9009\u9879')),
                ('csort', models.IntegerField()),
                ('num', models.IntegerField()),
            ],
            options={
                'db_table': 'examination_statistics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.IntegerField()),
                ('choice', models.IntegerField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortnum', models.IntegerField(default=1, verbose_name='\u5e8f\u53f7')),
                ('text', models.CharField(max_length=128, verbose_name='\u9009\u9879')),
                ('tags', models.CharField(blank=True, editable=False, max_length=64, verbose_name='Tags')),
            ],
            options={
                'verbose_name': '\u9009\u9879',
                'verbose_name_plural': '\u9009\u9879',
            },
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53d1\u5e03')),
                ('take_nums', models.IntegerField(default=0, verbose_name='\u53c2\u4e0e\u4eba\u6570')),
                ('type', models.CharField(choices=[(b'fixed', '\u56fa\u5b9a'), (b'random', '\u968f\u673a')], max_length=32, verbose_name='\u7c7b\u578b')),
                ('question_nums', models.IntegerField(default=0, verbose_name='\u8bd5\u9898\u6570')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.CourseOld', verbose_name='\u8bd5\u5377')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u8bd5\u9898',
                'verbose_name_plural': '\u8bfe\u7a0b\u8bd5\u9898',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortnum', models.IntegerField(default=1, verbose_name='\u5e8f\u53f7')),
                ('type', models.CharField(choices=[(b'radio', '\u5355\u9009'), (b'checkbox', '\u591a\u9009'), (b'star', '\u6253\u661f'), (b'text', '\u95ee\u7b54')], max_length=32, verbose_name='\u9898\u578b')),
                ('text', models.CharField(max_length=128, verbose_name='\u95ee\u9898')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.CourseOld', verbose_name='\u8bfe\u7a0b')),
            ],
            options={
                'verbose_name': '\u95ee\u9898',
                'verbose_name_plural': '\u95ee\u9898',
            },
        ),
        migrations.CreateModel(
            name='TakeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6d4b\u8bd5\u65f6\u95f4')),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Examination', verbose_name='\u6d4b\u8bd5')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examination_user_id', to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u8bb0\u5f55',
                'verbose_name_plural': '\u8bb0\u5f55',
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='runinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.TakeInfo'),
        ),
        migrations.CreateModel(
            name='PublishedExamination',
            fields=[
            ],
            options={
                'verbose_name': '\u7edf\u8ba1',
                'proxy': True,
                'verbose_name_plural': '\u7edf\u8ba1',
            },
            bases=('examination.examination',),
        ),
    ]
