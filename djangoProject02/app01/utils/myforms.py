from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app01.utils.encrypt import md5
from app01.models import UserInfo, PrettyNum, Admin
from app01.utils.bootstrapdodelform import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    # 字段格式限制
    username = forms.CharField(label="用户名", min_length=4, max_length=10)
    password = forms.CharField(label="密码", min_length=8)

    class Meta:
        model = UserInfo
        fields = ["username", "password", "age", "account", "create_time", "depart", "gender"]


# 因为添加号码和验证号码的逻辑不一样所以需要写两个类
class PrettyNumAddModelForm(BootStrapModelForm):
    # 数据验证方法1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(regex=r"^1[3-9]\d{9}$", message="手机号格式错误")]
    )

    class Meta:
        model = PrettyNum
        # fields = ["mobile", "price", "level", "state"]
        fields = "__all__"
        # exclude = ["level"]

    # 数据验证方法2---钩子方法
    def clean_mobile(self):
        # 获取当前电话号
        str_mobile = self.cleaned_data["mobile"]
        # if not mobile.match(r"^1[3-9]\d{9}"):
        #     raise ValidationError("格式错误")
        # 不能有重复手机号 Ture/False
        exists = PrettyNum.objects.filter(mobile=str_mobile).exists()
        print(exists)
        if not exists:
            return str_mobile
        raise ValidationError("手机号已存在")


class PrettyNumEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(regex=r"^1[3-9]\d{9}$", message="手机号格式错误")],
        # disabled=True 设置显示但不可修改
    )

    class Meta:
        model = PrettyNum
        fields = "__all__"

    def clean_mobile(self):
        str_mobile = self.cleaned_data["mobile"]
        # 获取当前编辑对象（行）的ID-PrimaryKey
        # self.instance.pk
        # 除自己外不能有重复手机号
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=str_mobile).exists()
        print(self.instance.pk, exists)
        if exists:
            raise ValidationError("手机号已存在")
        return str_mobile


class AdminAddModelForm(BootStrapModelForm):
    name = forms.CharField(
        label="管理员名称",
        validators=[RegexValidator(regex=r'^[A-Z].*', message="英文且首字母必须大写")]
    )
    # 数据库中无该字段 额外创建的一个field
    confirm_pwd = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Admin
        fields = "__all__"
        widgets = {
            "pwd": forms.PasswordInput(render_value=True)  # render_value=True 的作用是前端验证错误时保留上次输入数据
        }

    def clean_name(self):
        str_name = self.cleaned_data["name"]
        exists = Admin.objects.filter(name=str_name).exists()
        print(exists)
        if not exists:
            return str_name
        raise ValidationError("该名称已存在")

    def clean_pwd(self):
        str_pwd = self.cleaned_data["pwd"]
        # 返回什么 此字段以后保存到数据库就是什么
        return md5(str_pwd)

    def clean_confirm_pwd(self):
        # cleaned_data会拿到所有的输入数据 组装成一个字典
        str_pwd = self.cleaned_data.get("pwd")
        str_pwd2 = md5(self.cleaned_data.get("confirm_pwd"))
        print(str_pwd, str_pwd2)
        if str_pwd != str_pwd2:
            raise ValidationError("确认密码不一致")
        # 暂时没用 因为本字段不保存到数据库
        return str_pwd2


class AdminEditModelForm(BootStrapModelForm):
    name = forms.CharField(label="管理员名称",
                           validators=[RegexValidator(regex=r'^[A-Z].*', message="英文且首字母必须大写")])

    class Meta:
        model = Admin
        fields = ["name"]

    def clean_name(self):
        str_name = self.cleaned_data["name"]
        exists = Admin.objects.exclude(id=self.instance.pk).filter(name=str_name).exists()
        print(self.instance.pk, exists)
        if not exists:
            return str_name
        raise ValidationError("该名称已占用，请尝试其它名称")


class AdminResetModelForm(BootStrapModelForm):
    confirm_pwd = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Admin
        fields = ["pwd", "confirm_pwd"]
        widgets = {
            "pwd": forms.PasswordInput(render_value=True)  # render_value=True 的作用是前端验证错误时保留上次输入数据
        }

    def clean_pwd(self):
        str_pwd = self.cleaned_data["pwd"]
        # 实现修改密码不能与原密码一致
        md5_pwd = md5(str_pwd)
        if Admin.objects.filter(id=self.instance.pk, pwd=md5_pwd).exists():
            raise ValidationError("修改密码不能与原密码一致")
        return md5_pwd

    def clean_confirm_pwd(self):
        # cleaned_data会拿到所有的输入数据 组装成一个字典
        str_pwd = self.cleaned_data.get("pwd")
        str_pwd2 = md5(self.cleaned_data.get("confirm_pwd"))
        print(str_pwd, str_pwd2)
        if str_pwd != str_pwd2:
            raise ValidationError("确认密码不一致")
        # 暂时没用 因为本字段不保存到数据库
        return str_pwd2
