from django.shortcuts import render, redirect
from app01.utils.myforms import PrettyNumAddModelForm, PrettyNumEditModelForm
from app01.utils.pagination import Pagination
from app01.models import PrettyNum

"""靓号管理"""


def pnumber_list(request):
    """靓号列表"""
    # for i in range(300):
    #     PrettyNum.objects.create(mobile="12345678911", price=20, level=1, state=1)

    data_dict = {}
    # 获取模糊查询的get请求，无get请求时默认空字符串""
    search_data = request.GET.get("search", "")
    if search_data:
        # 字典数据赋值
        data_dict["mobile__contains"] = search_data
    # .filter(aaa="xxx", bbb="xxx", ccc="xxx")
    # 可以写成字典形式
    # data_dict={aaa="xxx", bbb="xxx", ccc="xxx"}
    # 然后如下 效果相同
    queryset = PrettyNum.objects.filter(**data_dict).order_by("-level")  # 模糊查询+降序 当value为空时 filter(空)=all()
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset

    page_str = page_object.html()

    content = {
        "search_data": search_data,
        "models": page_queryset,  # 分页完的数据
        "page_str": page_str,  # 生成页码 替换html占位符中内容
    }
    return render(request, "pnumber_list.html", content)


def pnumber_add(request):
    """添加靓号"""
    if request.method == "GET":
        form = PrettyNumAddModelForm()
        return render(request, "change.html", {"title": "添加靓号", "form": form})
    form = PrettyNumAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pnumber/list/")
    else:
        return render(request, "change.html", {"title": "添加靓号", "form": form})


def pnumber_edit(request, nid):
    """编辑靓号"""
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNumEditModelForm(instance=row_object)  # instance=row_object输入框中显示默认值
        return render(request, "pnumber_edit.html", {"form": form})
    form = PrettyNumEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pnumber/list/")
    else:
        return render(request, "pnumber_edit.html", {"form": form})


def pnumber_delete(request, nid):
    """删除靓号"""
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pnumber/list/")
