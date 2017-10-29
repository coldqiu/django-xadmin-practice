# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/12 0012 10:03'


import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'Email', 'send_type', 'send_time']
    search_fields = ['code', 'Email', 'send_type']
    list_filter = ['code', 'Email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "ColorOnlin 后台管理系统"
    site_footer = "ColorOnlne"
    menu_style = "accordion"


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
