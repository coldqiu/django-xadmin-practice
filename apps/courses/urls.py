# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/21 0021 19:21'

from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddComentsView,CoursePlayView

urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),

    #添加评论，不需要在这里传参数，在Ajax里传了
    url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),

    url(r'^video/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="course_play"),



]