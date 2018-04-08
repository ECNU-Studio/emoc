# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-04 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u95ee\u9898', 'verbose_name_plural': '\u95ee\u9898'},
        ),
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'permissions': (('export', 'Can export questionnaire answers'), ('management', 'Management Tools')), 'verbose_name': '\u95ee\u5377', 'verbose_name_plural': '\u95ee\u5377'},
        ),
        migrations.AlterModelOptions(
            name='runinfo',
            options={'verbose_name': '\u8bb0\u5f55', 'verbose_name_plural': '\u8bb0\u5f55'},
        ),
        migrations.AlterField(
            model_name='choice',
            name='sortnum',
            field=models.IntegerField(default=1, verbose_name='\u5e8f\u53f7'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='tags',
            field=models.CharField(blank=True, editable=False, max_length=64, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=128, verbose_name='\u9009\u9879'),
        ),
        migrations.AlterField(
            model_name='question',
            name='chice_text',
            field=models.TextField(blank=True, editable=False, help_text='\u6bcf\u4e2a\u9009\u9879\u8f93\u5165\u540e\u8bf7\u6362\u884c', null=True, verbose_name='\u9009\u9879'),
        ),
    ]