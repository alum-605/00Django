import json
import random
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Order
from app01.utils.bootstrapdodelform import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['order_id', 'user_o']


def order_list(request):
    """订单列表"""
    models = Order.objects.all().order_by('-id')
    page_obj = Pagination(request, models)
    form = OrderModelForm()
    context = {
        'models': page_obj.page_queryset,
        'form': form,
        'page_str': page_obj.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """添加订单(Ajax请求)"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 因为 OrderModelForm中设置了exclude = ['order_id', 'user'] 导致添加界面没有order_id输入框
        # 此时form的order_id默认为null
        """tips：使用instace时找对应字段必须使用实际保存在数据库中的字段名"""
        # 设置动态自动生成order_id
        form.instance.order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

        # 获取当前登陆用户的id赋给user_o
        form.instance.user_o_id = request.session['info']['id']

        form.save()
        # 此处使用的ModelForm自带的error配置 是一个字典，所以前端用v[0]
        data_dict = {"status": True, "error": form.errors}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


@csrf_exempt
def order_delete(request):
    """删除订单"""
    did = request.POST.get("did")
    # 判断订单是否存在
    exists = Order.objects.filter(id=did).exists()
    if not exists:
        data_dict = {"status": False, "error": "订单数据不存在"}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    Order.objects.filter(id=did).delete()
    data_dict = {"status": True}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


@csrf_exempt
def order_edit_detail(request):
    """编辑订单"""

    """ 方式1
    did = request.POST.get("did")
    row_obj = Order.objects.filter(id=did).first()  # 此ModelForm对象无法通过JSON序列化返回到前端
    if not row_obj:
        return JsonResponse({"status": False, "error": "订单数据不存在"})
    # 思路1 手动维护一个字典
    result = {
        "status": True,
        "data": {
            "id": row_obj.id,
            "order_id": row_obj.order_id,
            "name": row_obj.name,
            "price": row_obj.price,
            "status": row_obj.status,
            "user_o_id": row_obj.user_o_id,
        },
    }
    return JsonResponse(result)
    """

    # 方式2
    did = request.POST.get("did")
    # 思路2 通过.values("属性1", "属性2") 获取到的就是一个字典对象
    # 此处和下方order_edit的区别：
    # 此处要查询存在后将数据以json形式返回前端展示到对话框中，而不.value拿到的是一个ModelForm格式无法JSON序列化
    row_dict = Order.objects.filter(id=did).values("name", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "tips": "订单数据不存在"})
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    eid = request.GET.get("eid")
    row_obj = Order.objects.filter(id=eid).first()
    # print(eid, row_obj)
    if not row_obj:
        return JsonResponse({"status": False, "tips": "订单数据不存在2"})
    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


"""想要去数据库中获取数据时：对象/字典"""
# 对象，当前行的所有数据。
# row_object = models.Order.objects.filter(id=uid).first()
# row_object.id
# row_object.title

# 字典，{"id":1,"title":"xx"}
# row_dict = models.Order.objects.filter(id=uid).values("id", "title").first()

# queryset = [obj,obj,obj,]
# queryset = models.Order.objects.all()

# queryset = [ {'id':1,'title':"xx"},{'id':2,'title':"xx"}, ]
# queryset = models.Order.objects.all().values("id", "title")

# queryset = [ (1,"xx"),(2,"xxx"), ]
# queryset = models.Order.objects.all().values_list("id", "title")
