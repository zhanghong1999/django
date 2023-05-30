from django.shortcuts import render, redirect
from employee_web.models import Department


# 部门列表
def department_list(request):
    data_list = Department.objects.all()
    return render(request, "department_list.html", {"data_list": data_list})


# 新建部门
def department_add(request):
    if request.method == "GET":
        return render(request, "department_add.html")
    else:
        # 获得表单提交的title
        title = request.POST.get("title")
        # 数据添加到数据库中
        Department.objects.create(title=title)
        return redirect("/department/list/")


# 删除部门
def department_delete(request):
    nid = request.GET.get("nid")
    # 数据从数据库中删除
    Department.objects.filter(id=nid).delete()
    return redirect("/department/list/")


# 修改部门
def department_edit(request, nid):
    if request.method == "GET":
        # 根据nid得到该行数据
        data = Department.objects.filter(id=nid).first()
        return render(request, "department_edit.html", {"data": data})
    else:
        title = request.POST.get("title")
        # 数据添加到数据库中
        Department.objects.filter(id=nid).update(title=title)
        return redirect("/department/list/")
