# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/12 0012 10:02'

import xadmin
from .models import UserAsk,UserFavorite,UserMessage,CourseComments,UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'add_time']
    search_fields = ['name', 'mobile']
    list_filter = ['name', 'mobile', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields =['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'has_read', 'message', 'add_time']
    search_fields = ['user', 'has_read', 'message']
    list_filter = ['user', 'has_read', 'message', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
