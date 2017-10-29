# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/23 0023 23:04'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMinxin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMinxin, self).dispatch(request, *args, **kwargs)

