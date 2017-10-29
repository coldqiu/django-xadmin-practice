# _*_ coding: utf-8 _*_

__author__ = 'jeff-L'
__date__ = '2017/10/16 0016 10:59'
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from ColorOnline.settings import EMAIL_FROM


#用于生成随机字符串的函数,不知为什么，这个函数只会执行一次
def random_str(randomlength):
    str = ''
    chars = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.Email = email
    email_record.send_type = send_type
    email_record.save()
    #保存用户的邮箱和邮件类型，生成一个随机字符串并且三者都保存至数据库
    #便于邮件激活时确认用户身份
    #定义邮件内容
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "ColorOnline网站激活邮件"
        email_body = "点击链接激活您的ColorOnline账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == "forget":
        email_title = "ColorOnline网站邮件找回密码"
        email_body = "ColorOnline:点击链接重制您账号的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == "update_email":
        email_title = "ColorOnline网站修改邮箱"
        email_body = "ColorOnline:你的邮箱验证码：{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
