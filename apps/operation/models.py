# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import Userprofile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机号")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name

class CourseComments(models.Model):
    '''课程评论，涉及用户和课程评论'''
    user = models.ForeignKey(Userprofile, verbose_name=u"用户", default='')
    course = models.ForeignKey(Course, verbose_name=u"课程", default='')
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(Userprofile, verbose_name=u"用户", default='')
    fav_id = models.IntegerField(default=0, verbose_name=u"收藏id")
    fav_type = models.IntegerField(verbose_name=u'收藏类型', choices=((1,"课程"),(3,"教师"),(2,"机构")))
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    '''user 传入的是id 0表示系统发的， 具体id，表示具体用户'''
    user = models.IntegerField(default=0, verbose_name=u"用户id")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(Userprofile, verbose_name=u"用户", default='')
    course = models.ForeignKey(Course, verbose_name=u"课程", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name