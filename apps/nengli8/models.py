# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Course(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='课程名字', db_column='name')

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'courses'


class User(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='用户名', db_column='name')

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'users'