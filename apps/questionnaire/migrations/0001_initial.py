# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-21 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nengli8', '0002_userold'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionnaireStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionnaire', models.IntegerField()),
                ('name', models.CharField(max_length=128, verbose_name='\u95ee\u5377\u6807\u9898')),
                ('question', models.IntegerField()),
                ('question_text', models.CharField(max_length=128, verbose_name='\u95ee\u9898')),
                ('qsort', models.IntegerField()),
                ('type', models.CharField(max_length=32)),
                ('choice', models.IntegerField()),
                ('choice_text', models.CharField(max_length=128, verbose_name='\u9009\u9879')),
                ('csort', models.IntegerField()),
                ('sum', models.IntegerField()),
                ('percent', models.IntegerField()),
            ],
            options={
                'db_table': 'questionnaire_statistics',
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
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortnum', models.IntegerField(default=1, verbose_name='\u5e8f\u53f7')),
                ('type', models.CharField(choices=[(b'radio', '\u5355\u9009'), (b'checkbox', '\u591a\u9009'), (b'star', '\u6253\u661f'), (b'text', '\u95ee\u7b54')], max_length=32, verbose_name='\u9898\u578b')),
                ('text', models.CharField(max_length=128, verbose_name='\u95ee\u9898')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u95ee\u9898',
                'verbose_name_plural': '\u95ee\u9898',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53d1\u5e03')),
                ('take_nums', models.IntegerField(default=0, verbose_name='\u53c2\u4e0e\u4eba\u6570')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nengli8.CourseOld', verbose_name='\u95ee\u5377')),
            ],
            options={
                'verbose_name': '\u95ee\u5377',
                'verbose_name_plural': '\u95ee\u5377',
                'permissions': (('export', 'Can export questionnaire answers'), ('management', 'Management Tools')),
            },
        ),
        migrations.CreateModel(
            name='RunInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u95ee\u5377\u65f6\u95f4')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Questionnaire', verbose_name='\u95ee\u5377')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire_user_id', to='nengli8.UserOld', verbose_name='\u95ee\u5377\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u8bb0\u5f55',
                'verbose_name_plural': '\u8bb0\u5f55',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Questionnaire', verbose_name='\u95ee\u5377'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='runinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.RunInfo'),
        ),
    ]
