# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/20 0020 12:15'

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    #课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 课程列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    #教师详情页
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]