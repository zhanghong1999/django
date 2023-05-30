from django.shortcuts import render, redirect
from employee_web.models import PrettyNum
from employee_web.utils.form import NumModelForm, NumEditModelForm


# 号码列表
def num_list(request):
    # 实现根据号码的搜索功能
    data = {}
    search_data = request.GET.get("q")
    if search_data:
        data = {"mobile__contains": search_data}
    else:
        search_data = ""

    # 分页功能
    from employee_web.utils.page import Pagination
    data_list = PrettyNum.objects.filter(**data)
    # 实例化分页对象
    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()

    context = {
        "search_data": search_data,  # 搜索
        "data_list": page_data_list,  # 分页后的数据
        "page_string": page_string  # 页码
    }
    return render(request, "num_list.html", context)


# 添加号码
def num_add(request):
    if request.method == "GET":
        form = NumModelForm()
        return render(request, "num_add.html", {"form": form})

    form = NumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/num/list/")

    return render(request, "num_add.html", {"form": form})


# 修改号码(无法修改手机号、修改的号码不重复)
def num_edit(request, nid):
    data = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumEditModelForm(instance=data)
        return render(request, "num_edit.html", {"form": form})

    form = NumEditModelForm(data=request.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect("/num/list/")

    return render(request, "num_edit.html", {"form": form})


# 删除号码
def num_delete(request, nid):
    # 数据从数据库中删除
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/num/list/")
