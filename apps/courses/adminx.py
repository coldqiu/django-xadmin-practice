# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/12 0012 10:02'


from .models import Course
from .models import Lesson
from .models import Video
from .models import CourseResource

import xadmin

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'image']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = []
    search_field = []
    list_filter = []


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)