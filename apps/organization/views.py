# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import CityDict, CourseOrg, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        #所有机构
        all_orgs = CourseOrg.objects.all()

        #所有城市
        all_cites = CityDict.objects.all()

        #机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                       Q(desc__icontains=search_keywords))

        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        #取出从前端传来的筛选城市,city_id的由来，机构里的city字段只是一个外键
        city_id= request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
            #把后台选中的id 传回前端，让他知道自己被选中了，好给选中的一样式

        #对培训机构的类别做筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        #分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)


        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cites,
            "org_nums": org_nums,
            #把选中的id传回前端，完成比对
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort

        })

class AddUserAskView(View):
    '''用户咨询'''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

class OrgHomeView(View):
    '''机构首页'''
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))

        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        #判断用户是否等登录
        if request.user.is_authenticated():
            #判断用户是否收藏,前端传来的fav_type=2，而机构在数据库的fav-type=3,导致页面刷新后丢失机构已收藏的状态，那段ajax看不懂，
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html', {
            'all_courese': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })

class OrgCourseView(View):
    '''机构课程首页'''

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courese': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav

        })

class OrgDescView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })

class OrgTeacherView(View):
    '''机构教师'''

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
            'has_fav': has_fav,

        })


class AddFavView(View):
    '''
    用户收藏， 以及用户取消收藏
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户是否为登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id = int(fav_id), fav_type = int(fav_type))
        if exist_records:
            #记录已经存在，表示用户取消 收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -=1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums += 1
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums += 1
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums += 1
                teacher.save()

            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 教师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_teachers = all_teachers.order_by("-students")
            elif sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        #取出人气前三人
        sorted_teacher = Teacher.objects.order_by("-click_nums")[:3]

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 3, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html",{
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        #教师排行榜，取出前三
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        #左右两个收藏
        has_teacher_faved = False
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_courses":all_courses,
            "sorted_teacher": sorted_teacher,
            "has_org_faved": has_org_faved,
            "has_teacher_faved": has_teacher_faved

        })

