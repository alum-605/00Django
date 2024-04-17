from django.shortcuts import render, redirect

from app01.utils.myforms import UserModelForm
from app01.utils.pagination import Pagination
from app01.models import Department, UserInfo

"""员工管理"""


def user_list(request):
    """员工列表"""
    # for i in range(100):
    #     UserInfo.objects.create(
    #     username="武佩奇", password="123321", age=28, account=1000.99, create_time="2019-05-30", depart_id=12, gender=1)
    queryset = models = UserInfo.objects.all()
    page_object = Pagination(request, queryset)
    return render(request, "user_list.html", {"models": page_object.page_queryset, "page_str": page_object.html()})


def user_add(request):
    """添加员工"""
    if request.method == "GET":
        content = {
            "gender_choices": UserInfo.gender_choice,
            "depart_list": Department.objects.all()
        }
        return render(request, "user_add.html", content)
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    act = request.POST.get("account")
    ctime = request.POST.get("creat_time")
    did = request.POST.get("DepartName")
    gender = request.POST.get("gender")

    UserInfo.objects.create(username=name, password=pwd, age=age, account=act, create_time=ctime, depart_id=did,
                            gender=gender)
    return redirect("/user/list/")


# ########### ModelForm实现增删改查 ############

""" 
class UserModelForm(forms.ModelForm):
    # 字段格式限制
    username = forms.CharField(label="用户名", min_length=4, max_length=10)
    password = forms.CharField(label="密码", min_length=8)

    class Meta:
        model = UserInfo
        fields = ["username", "password", "age", "account", "create_time", "depart", "gender"]
        # weights插件添加样式
        # widgets = {
        #     "username": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "account ": forms.TextInput(attrs={"class": "form-control"})
        #     .....
        # }  简化如下

    # 重写构造方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到每一个插件添加class="form-control"样式
        for name, field in self.fields.items():
            # 单独对某一个字段设置
            # if name == "password"
            #   continue
            # field.widget.attrs = {"class": "form-control", "placeholder": field.label}

            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }
"""


# 引入继承思想后


def user_model_form_add(request):
    """添加用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # POST提交(新增) 数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        # 校验失败 显示错误信息，
        return render(request, "user_model_form_add.html", {"form": form})


def user_model_form_edit(request, nid):
    """编辑用户"""

    # 根据id获取要编辑的那一行数据
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # ModelForm简化 html中value="xxx" 在input中显示默认值的过程
        form = UserModelForm(instance=row_object)
        return render(request, "user_model_form_edit.html", {"form": form})

    # POST提交(修改) 数据校验
    # 不加instance 则会变成新建数据；使用instace即可指明替换(更新)哪一条数据
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        # 校验失败 显示错误信息，
        return render(request, "user_model_form_edit.html", {"form": form})


def user_model_form_delete(request, nid):
    """删除用户"""
    UserInfo.objects.get(id=nid).delete()
    return redirect("/user/list/")
