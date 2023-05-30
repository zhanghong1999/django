import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from employee_web.utils.bootstrap import BootstrapModelForm
from employee_web.models import News
from employee_web.utils.page import Pagination


class NewModelForm(BootstrapModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
            # "detail": forms.Textarea
        }


def new_list(request):

    form = NewModelForm()

    # 分页功能
    data_list = News.objects.all()
    # 实例化分页对象
    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()

    context = {
        "data_list": page_data_list,  # 分页后的数据
        "page_string": page_string,  # 页码
        "form": form
    }

    return render(request, "new_list.html", context)


@csrf_exempt  # 免除csrf的认证
def new_ajax(request):
    # print(request.POST)
    # 对发送过来的数据进行校验(ModelForm)
    form = NewModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    # print(type(form.errors)) ErrorDict格式
    data_dict = {"status": False, "error": form.errors}
    # status的状态表示是否添加到数据库
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

