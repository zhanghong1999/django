from django.shortcuts import render, redirect
from employee_web.models import Admin
from employee_web.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from employee_web.utils.page import Pagination


# 管理员列表

def admin_list(request):
    """
    用户登录后才能看到该页面--->改用中间件
    # 检查用户是否登录
    # 用户发来请求，获取cookie中的随机字符串session id，
    # 检查session中是否有该session id
    # request.session.get("info")获得当初写入的信息（id和name的字典）
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    """

    data = {}
    search_data = request.GET.get("q")
    if search_data:
        data = {"username__contains": search_data}
    else:
        search_data = ""
    data_list = Admin.objects.filter(**data)
    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()
    context = {
        "search_data": search_data,
        "data_list": page_data_list,
        "page_string": page_string
    }
    return render(request, "admin_list.html", context)


# 添加管理员
def admin_add(request):
    title = "添加管理员"
    if request.method == "GET":
        # 自动生成input标签
        form = AdminModelForm()
        return render(request, "ha.html", {"form": form, "title": title})
    else:
        # 获得表单提交的数据
        form = AdminModelForm(data=request.POST)
        # 数据校验
        if form.is_valid():
            # 数据添加到数据库中
            # form.cleaned_data 通过验证的数据
            form.save()
            return redirect("/admin/list/")
        else:
            # 显示错误信息
            return render(request, "ha.html", {"form": form, "title": title})


# 修改管理员
def admin_edit(request, nid):
    # 根据ID，到数据库获取要编辑的那行数据的对象
    title = "修改管理员"
    # 数据为object或None
    obj = Admin.objects.filter(id=nid).first()
    # 数据是否存在
    if not obj:
        return render(request, "error.html", {"error": "数据不存在"})

    if request.method == "GET":
        form = AdminEditModelForm(instance=obj)
        # 自动生成input标签，instance=obj使input框内的内容显示原来的内容
        return render(request, "ha.html", {"form": form, "title": title})

    # 获得表单提交的数据
    form = AdminEditModelForm(data=request.POST, instance=obj)  # 修改一定要有instance=obj，不然就成了新增
    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    else:
        # 显示错误信息
        return render(request, "ha.html", {"form": form, "title": title})


# 删除管理员
def admin_delete(request, nid):
    # 数据从数据库中删除
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


# 重置密码
def admin_reset(request, nid):

    # 数据为object或None
    obj = Admin.objects.filter(id=nid).first()
    # 数据是否存在
    if not obj:
        return render(request, "error.html", {"error": "数据不存在"})

    title = "重置密码-{}".format(obj.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        # 自动生成input标签，instance=obj使input框内的内容显示原来的内容
        return render(request, "ha.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=obj)  # 修改一定要有instance=obj，不然就成了新增
    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "ha.html", {"form": form, "title": title})

