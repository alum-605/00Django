from django.shortcuts import render, redirect

from app01.models import Admin
from app01.utils.pagination import Pagination
from app01.utils.myforms import AdminAddModelForm, AdminEditModelForm, AdminResetModelForm


def login(request):
    """管理员登陆"""
    pass


def admin_list(request):
    """管理员列表"""
    queryset = Admin.objects.all()
    page_object = Pagination(request, queryset)
    content = {
        'models': queryset,
        'page_object': page_object.page_queryset,
        'page_str': page_object.html()
    }
    # return render(request, 'admin_list.html', content)
    return render(request, 'admin/admin_list.html', content)


def admin_add(request):
    """添加管理员"""
    if request.method == 'GET':
        form = AdminAddModelForm()
        return render(request, 'change.html', {'title': "添加管理员", 'form': form})
    form = AdminAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    else:
        return render(request, "change.html", {'title': "添加管理员", 'form': form})


def admin_edit(request, nid):
    """编辑管理员"""
    title = "编辑管理员"
    row_obj = Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, 'error.html', {"error_msg": "请求编辑的管理员不存在"})
    else:
        if request.method == "GET":
            form = AdminEditModelForm(instance=row_obj)
            return render(request, "change.html", {'title': title, 'form': form})
        else:
            form = AdminEditModelForm(data=request.POST, instance=row_obj)
            if form.is_valid():
                form.save()
                return redirect("/admin/list")
            return render(request, "change.html", {'title': title, 'form': form})


def admin_delete(request, nid):
    """删除管理员"""
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    """重置密码"""
    row_obj = Admin.objects.filter(id=nid).first()
    title = "重置管理员密码--{}".format(row_obj.name)
    if not row_obj:
        return render(request, 'error.html', {"error_msg": "请求重置密码的管理员不存在"})
    else:
        if request.method == "GET":
            form = AdminResetModelForm()
            return render(request, "change.html", {'title': title, 'form': form})
        form = AdminResetModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "change.html", {'title': title, 'form': form})
