# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Course(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='课程名字')

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'courses'



class User(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='用户名')

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'users'