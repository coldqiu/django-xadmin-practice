# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/15 0015 19:13'
from django import forms
from captcha.fields import CaptchaField
from .models import Userprofile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=3)
    password2 = forms.CharField(required=True, min_length=3)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']