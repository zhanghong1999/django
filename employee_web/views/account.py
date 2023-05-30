from django.shortcuts import render, redirect, HttpResponse
from django import forms
from employee_web.utils.bootstrap import BootstrapForm
from employee_web.utils.encrypt import md5
from employee_web.models import Admin
from employee_web.utils.image_code import check_code


# 之前采用modelform，现在尝试form
class LoginForm(BootstrapForm):
    # form中定义的名字与数据库的字段名一致
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True  # 必填（默认是True）
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )
    image_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        # 钩子方法，密码加密
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


"""
实现效果如同
from employee_web.models import Admin
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["username","password"]
"""


# 用户登录
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 获得表单提交的数据
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码
        # 输入的验证码
        user_input = form.cleaned_data.pop("image_code")
        # 用pop--->后续到数据库校验用户名和密码，不需要验证码
        # 写入到session中的验证码， 如果超时，就为""
        code = request.session.get("image_code", "")
        if user_input.upper() != code.upper():
            form.add_error("image_code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # modelform关联数据库，有model.save()
        # form得到提交的数据，form.cleaned_data，以字典的形式
        # 数据库查找是否存在数据，获得与输入一致的数据库中的对象或None
        obj = Admin.objects.filter(**form.cleaned_data).first()
        if not obj:
            # 没有数据None--->用户名或密码错误
            # 错误信息用户名或密码错误展示在字段password下方
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        # 有数据--->用户名和密码正确
        # 网站生成随机字符串作为session id，写到用户浏览器的cookie中，
        # session 数据在数据库，数据加密
        request.session["info"] = {"id": obj.id, "username": obj.username}
        # 存储当前用户信息（id，name），字典形式

        request.session.set_expiry(60*60*24*7)
        # session保存7天

        return redirect("/admin/list")
    return render(request, "login.html", {"form": form})


# 用户注销
def logout(request):
    request.session.clear()
    # request.session.flush()
    return redirect("/login/")


"""
session的清除有clear() 和 flush()两种方法
    session.flush()的作用就是将缓存的session数据进行清理，同时清理数据库
    session.clear()的作用就是清除session中的缓存数据，不会管数据和数据库的同步
"""

from io import BytesIO


def image_code(request):
    # 调用函数，生成验证码图片和其中的内容
    img, code_str = check_code()
    # print(code_str)
    # 创建一个内存中的文件
    stream = BytesIO()
    # 将验证码图片写入文件
    img.save(stream, 'png')

    # 将验证码内容写入到session中
    # 以便于后续获取验证码再进行校验
    request.session["image_code"] = code_str
    # 设置60s超时
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue())
