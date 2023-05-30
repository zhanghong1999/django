"""
URL configuration for employee_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employee_web.views import department, user, number, admin, account, ajax, new, order

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 部门管理
    path('department/list/', department.department_list),
    path('department/add/', department.department_add),
    path('department/delete/', department.department_delete),

    # path('department/edit/', views.department_edit),
    # 携带id 此时网址为.../department/一个整型数字/edit
    path('department/<int:nid>/edit/', department.department_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add1/', user.user_add1),
    path('user/add2/', user.user_add2),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 号码管理
    path('num/list/', number.num_list),
    path('num/add/', number.num_add),
    path('num/<int:nid>/edit/', number.num_edit),
    path('num/<int:nid>/delete/', number.num_delete),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # ajax
    path('learn/ajax/', ajax.learn_ajax),
    path('test/ajax/', ajax.test_ajax),

    # 应用ajax---消息管理
    path('new/', new.new_list),
    path('new/ajax/', new.new_ajax),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/del/', order.order_del),
    path('order/<int:uid>/edit1/', order.order_edit1),
    path('order/detail/', order.order_detail),
    path('order/edit2/', order.order_edit2),

]
