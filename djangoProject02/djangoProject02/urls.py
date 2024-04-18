"""
URL configuration for djangoProject02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from app01.views import depart, user, pnumber, admin, login, task, order, chart, city

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # r'^media/(?P<path>.*)$' 指url以media/除换行符以外的所有字符

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/delete/<int:nid>/', depart.depart_delete),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),

    path('user/model/form/add/', user.user_model_form_add),
    path('user/model/form/<int:nid>/edit/', user.user_model_form_edit),
    path('user/model/form/<int:nid>/delete/', user.user_model_form_delete),

    # 靓号管理
    path('pnumber/list/', pnumber.pnumber_list),
    path('pnumber/add/', pnumber.pnumber_add),
    path('pnumber/<int:nid>/edit/', pnumber.pnumber_edit),
    path('pnumber/<int:nid>/delete/', pnumber.pnumber_delete),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 管理员登陆/注销
    path('login/', login.login),
    path('logout/', login.logout),
    path('image/code/', login.image_code),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/edit/detail/', order.order_edit_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('highcharts/scatter/', chart.highcharts_scatter),

    # 文件上传
    # path('upload/list/', upload.upload_list),
    # path('depart/multi/', depart.depart_multi),
    # path('upload/form1/', upload.upload_form1),
    # path('upload/form2/', upload.upload_form2),
    # path('upload/modelform/', upload.upload_modelform),

    # 路由分发
    path('upload/', include('app01.urls')),

    # 城市列表
    path('city/list/', city.city_list)

    #测试git

]
