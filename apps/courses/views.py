# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from utils.minxin_utils import LoginRequiredMinxin
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains = search_keywords) |
                                                    Q(desc__icontains = search_keywords) |
                                                    Q(detail__icontains = search_keywords))


        #课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses

        })

class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.click_nums += 1
        course.save()

        #课程详情页的收藏
        has_fav_org = False
        has_fav_course = False
        #判断用户是否登录
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course

        })


class CourseInfoView(LoginRequiredMinxin, View):
    #章节信息
    def get(self, request, course_id):
        #从数据库中一个课程对象
        course = Course.objects.get(id=int(course_id))

        course.students += 1
        course.save()

        #先判断用户与课程是否关联
        userAndcourse = UserCourse.objects.filter(user=request.user, course=course)
        if not userAndcourse:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        all_resources = CourseResource.objects.filter(course=course)
        #从表usercourse中取出包含该门课的所有记录，UserCourse对象
        user_courses = UserCourse.objects.filter(course=course)
        #取出学过该门课的所有学生的id，存在列表user_ids中
        user_ids = [user_course.user.id for user_course in user_courses]
        #从表usercourse中，取出user_ids里所有学生学过的所有课程，存在all_user_courses里
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #从UserCourse对象中取出所有课程的id，存在course_ids中
        course_ids = [user_course.course.id for user_course in user_courses]

        #取出点击量前五名
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]


        return render(request, "course-video.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses
        })


class CoursePlayView(LoginRequiredMinxin, View):
    #章节信息
    def get(self, request, video_id):
        #从数据库中一个视频对象
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        #先判断用户与课程是否关联
        userAndcourse = UserCourse.objects.filter(user=request.user, course=course)
        if not userAndcourse:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        all_resources = CourseResource.objects.filter(course=course)
        #从表usercourse中取出包含该门课的所有记录，UserCourse对象
        user_courses = UserCourse.objects.filter(course=course)
        #取出学过该门课的所有学生的id，存在列表user_ids中
        user_ids = [user_course.user.id for user_course in user_courses]
        #从表usercourse中，取出user_ids里所有学生学过的所有课程，存在all_user_courses里
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #从UserCourse对象中取出所有课程的id，存在course_ids中
        course_ids = [user_course.course.id for user_course in user_courses]

        #取出点击量前五名
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]


        return render(request, "course-play.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video
        })


class CourseCommentView(LoginRequiredMinxin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 先判断用户与课程是否关联
        userAndcourse = UserCourse.objects.filter(user=request.user, course=course)
        if not userAndcourse:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(course=course)
        # 取出学过该门课的所有学生的id，存在列表user_ids中
        user_ids = [user_course.user.id for user_course in user_courses]
        # 从表usercourse中，取出user_ids里所有学生学过的所有课程，存在all_user_courses里
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 从UserCourse对象中取出所有课程的id，存在course_ids中
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 取出点击量前五名
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, "course-comment.html", {
            "course": course,
            "all_comments": all_comments,
            "relate_courses": relate_courses

        })


class AddComentsView(View):
    '''
    用户添加评论
    '''
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户是否登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',  content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}',  content_type='application/json')
        else:
            return HttpResponse('{"status":"", "msg":"添加成功失败"}',  content_type='application/json')


