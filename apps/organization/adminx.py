# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'

import xadmin

from .models import CourseOrg,CityDict,Teacher


'''全部功能里都删除城市，才没有报错'''
class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year','work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields =['org', 'name', 'work_year','work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_year','work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
