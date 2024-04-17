import json

from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from app01.models import Task
from app01.utils.pagination import Pagination
from app01.utils.bootstrapdodelform import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            "detail": forms.TextInput
            # "detail": forms.Textarea
        }


@csrf_exempt
def task_list(request):
    """任务列表"""
    form = TaskModelForm()
    queryset = Task.objects.all().order_by('level', '-id')
    page_object = Pagination(request, queryset, page_size=5)
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_str": page_object.html()
    }
    return render(request, "task_list.html", context)


@csrf_exempt  # 免除csrf_token验证
def task_ajax(request):
    """
    print(request.GET)  # <QueryDict: {'n1': ['123'], 'n2': ['asda']}>
    print(request.POST)  # <QueryDict: {'n1': ['456'], 'n2': ['alum']}>
    将字典类型转换成易在网络中传输的json格式
    法2:简写
    data_dict = {"status": "success", "data": [11, 22, 33, 44]}
    return JsonResponse(data_dict)
    """
    # 法1:
    data_dict = {"status": "success", "data": [11, 22, 33, 44]}
    # json_dumps(dict)时，如果dict包含有汉字，一定加上ensure_ascii=False
    json_str = json.dumps(data_dict)
    # print(type(json_str))  # <class 'str'>

    print(request.POST)

    return HttpResponse(json_str)


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": "True", "error": form.errors}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    data_dict = {"status": "False", "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
