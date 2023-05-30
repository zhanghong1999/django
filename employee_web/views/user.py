from django.shortcuts import render, redirect
from employee_web.models import Department, UserInfo
from employee_web.utils.form import UserModelForm


# 员工列表
def user_list(request):
    data = {}
    search_data = request.GET.get("q")
    if search_data:
        data = {"name__contains": search_data}
    else:
        search_data = ""
    data_list = UserInfo.objects.filter(**data)
    """
        for obj in data_list:
        print(obj.time)  # 输出2013-01-01 00:00:00+00:00 type是datetime
        print(obj.time.strftime("%Y-%m-%d"))  # 输出2022-03-04 type是str
        print(obj.gender)  # 输出1/0
        print(obj.get_gender_display())  # 输出男/女
        # get_字段名_display()
        print(obj.depart_id)  # 输出Department object (1) 数据库中存储的字段名
        print(obj.depart.title)  # 输出IT部
        # obj.depart根据id自动去关联的表中获取相应的那行数据(包括id，title)。
    """
    from employee_web.utils.page import Pagination
    # 实例化分页对象
    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()

    context = {
        "search_data": search_data,  # 搜索
        "data_list": page_data_list,  # 分页后的数据
        "page_string": page_string  # 页码
    }

    return render(request, "user_list.html", context)


# 添加员工(原始方法)
def user_add1(request):
    if request.method == "GET":
        context = {
            "gender_choices": UserInfo.choice_gender,
            "department": Department.objects.all()
        }
        return render(request, "user_add1.html", context)
    else:
        # 获得表单提交的数据
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        money = request.POST.get("account")
        time = request.POST.get("time")
        department = request.POST.get("department")
        # 数据添加到数据库中
        UserInfo.objects.create(name=name, password=pwd, age=age, gender=gender, money=money, time=time,
                                depart_id=department)
        return redirect("/user/list/")


# 添加员工(ModelForm方法)
def user_add2(request):
    if request.method == "GET":
        form = UserModelForm()
        # 自动生成input标签
        return render(request, "user_add2.html", {"form": form})
    else:
        # 获得表单提交的数据
        form = UserModelForm(data=request.POST)
        # 数据校验
        if form.is_valid():
            # 数据添加到数据库中
            form.save()
            return redirect("/user/list/")
        else:
            # 显示错误信息
            return render(request, "user_add2.html", {"form": form})


# 修改员工
def user_edit(request, nid):
    if request.method == "GET":
        # 根据ID，到数据库获取要编辑的那行数据的对象
        obj = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=obj)
        # 自动生成input标签，instance=obj使input框内的内容显示原来的内容
        return render(request, "user_edit.html", {"form": form})
    else:
        obj = UserInfo.objects.filter(id=nid).first()
        # 获得表单提交的数据
        form = UserModelForm(data=request.POST, instance=obj)  # 修改一定要有instance=obj，不然就成了新增
        # 数据校验
        if form.is_valid():
            # 数据保存到数据库中（默认保存输入的所有数据）
            # 如果在新建的class不包含所有字段，想额外添加字段的值
            # form.instance.字段名 = 值
            # 如没有pwd，想额外增加pwd的值为1234
            # form.instance.pwd = "1234"
            form.save()
            return redirect("/user/list/")
        else:
            # 显示错误信息
            return render(request, "user_edit.html", {"form": form})


# 删除员工
def user_delete(request, nid):
    # 数据从数据库中删除
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
