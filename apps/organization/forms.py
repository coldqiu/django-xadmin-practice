# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/20 0020 11:57'
import re
from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''验证手机号是否合法'''
        #只是取出该字段
        mobile = self.cleaned_data['mobile']
        #网上下载的
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号非法", code="mobile_invalid")



