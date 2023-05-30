import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from employee_web.utils.bootstrap import BootstrapModelForm
from employee_web.models import Order
from employee_web.utils.page import Pagination


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = Order
        # fields = ["name", "price", "status", "user"]
        # exclude = ["oid", "user"]
        exclude = ["oid"]


def order_list(request):
    data_list = Order.objects.all()

    page_object = Pagination(request, data_list)
    page_data_list = page_object.page_data_list
    page_string = page_object.html()

    form = OrderModelForm()
    context = {
        "form": form,
        "data_list": page_data_list,
        "page_string": page_string
    }
    return render(request, "order_list.html", context)


@csrf_exempt  # 免除csrf的认证
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 用户为当前登录的管理员！！！
        # 无法实现，因为订单用户关联了UserInfo表而不是Admin表
        # form.instance.user_id = request.session["info"]["id"]
        # 订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    # print(type(form.errors)) ErrorDict格式
    data_dict = {"status": False, "error": form.errors}
    # status的状态表示是否已经添加到数据库
    return JsonResponse(data_dict)


def order_del(request):
    uid = request.GET.get("uid")
    flag = Order.objects.filter(id=uid).exists()
    if flag:
        Order.objects.filter(id=uid).delete()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    else:
        data_dict = {"status": False, "error": "删除失败，数据不存在"}
        return JsonResponse(data_dict)


@csrf_exempt  # 免除csrf的认证
def order_edit1(request, uid):
    obj = Order.objects.filter(id=uid).first()
    form = OrderModelForm(data=request.POST, instance=obj)
    if not obj:
        data_dict = {"status": False, "error": "数据不存在"}
        return JsonResponse(data_dict)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, "error": form.errors}
    # status的状态表示是否已经添加到数据库
    return JsonResponse(data_dict)


@csrf_exempt  # 免除csrf的认证
def order_edit2(request):
    uid = request.GET.get("uid")
    obj = Order.objects.filter(id=uid).first()
    if not obj:
        data_dict = {"status": False, "tips": "数据不存在"}
        return JsonResponse(data_dict)
    form = OrderModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, "error": form.errors}
    # status的状态表示是否已经添加到数据库
    return JsonResponse(data_dict)


# 根据id获得订单详细
@csrf_exempt  # 免除csrf的认证
def order_detail(request):
    # 方式一：
    """
    uid = request.GET.get("uid")
    obj = Order.objects.filter(id=uid).first()  # 从数据库中获得对象
    if not obj:
        data_dict = {"status": False, "error": "数据不存在"}
        return JsonResponse(data_dict)
    # 获得对象里的数据（对象没法通过JSON序列化响应给ajax请求）
    row_dict = {
        "name": obj.name,
        "price": obj.price,
        "status": obj.status,
        "user": obj.user_id
    }
    data_dict = {
        "status": True,
        "result": row_dict
    }
    return JsonResponse(data_dict)
    """

    # 方式二：
    uid = request.GET.get("uid")
    row_dict = Order.objects.filter(id=uid).values("name", "price", "status", "user").first()  # 从数据库中获得对象
    if not row_dict:
        data_dict = {"status": False, "error": "数据不存在"}
        return JsonResponse(data_dict)
    data_dict = {
        "status": True,
        "result": row_dict
    }
    return JsonResponse(data_dict)


"""
备注：
    obj = Order.objects.filter(id=uid).first()  # 当前行所有数据组成的对象
    obj.id ， obj.name 等
    obj = Order.objects.filter(id=uid).values("id","name"...).first()  # 得到一个字典
    {id:"1", name:"苹果", ...}
"""
