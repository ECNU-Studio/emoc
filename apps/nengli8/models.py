# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class CourseOld(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='课程名字')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'courses'


class UserOld(models.Model):
    # id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=52, verbose_name='账号', db_column='username')

    def __unicode__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'users'