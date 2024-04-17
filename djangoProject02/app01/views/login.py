from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01.models import Admin
from app01.utils.bootstrapdodelform import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from io import BytesIO


# 只做查询 用Form
class LoginForm(BootStrapForm):
    # required=True 不能为空 此项为默认设置 不写效果一样，设置允许为空可以修改为False
    name = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    pwd = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label="图片验证码", widget=forms.TextInput)

    def clean_pwd(self):
        str_pwd = self.cleaned_data["pwd"]
        md5_pwd = md5(str_pwd)
        return md5_pwd


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 获取到数据-字典
        # 去数据库中校验比对
        # 输入 aaa 123 adasd
        # 有 form.cleaned_data = {'name': 'aaa', 'pwd': '8c4d1a99e2ef83ac59236e2e215e3df2', 'code': 'adasd'}
        # compare_dict = {
        #     'name': form.cleaned_data['username'],
        #     'pwd': form.cleaned_data['pwd']}
        # login_obj = Admin.objects.filter(**compare_dict).first()

        # 验证码的校验
        # 不可以 user_input_code = form.cleaned_data['code'] 需要用pop将code从form.cleaned_dat中剔除，此后才可以去数据库中比对用户名和密码
        user_input_code = form.cleaned_data.pop('code')
        true_code = request.session.get('image_code', "")
        if true_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码输入错误")
            return render(request, 'login.html', {'form': form})

        # 验证码验证正确 验证用户名和密码
        login_obj = Admin.objects.filter(**form.cleaned_data).first()
        if not login_obj:
            form.add_error("pwd", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入服务器的session中（django中默认保存在Mysql中）
        request.session['info'] = {
            'id': login_obj.id,
            'loginname': login_obj.name,
        }
        # 用户登陆信息保存7天
        request.session.set_expiry(60*60*24*7)
        return redirect("/user/list/")
    # 输入数据非法 但是并没有对数据内容设置校验条件 因为这是登陆
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数生成图片
    img, code_str = check_code()
    # print(code_str)

    # 将验证码的字符串写入session中便于后续与用户输入的验证码进行比对
    request.session['image_code'] = code_str
    # 给session设置一60s超时
    request.session.set_expiry(60)

    # 创建一个内存文件
    stream = BytesIO()
    # .save()写到stream中以png格式
    img.save(stream, 'png')
    stream.getvalue()

    return HttpResponse(stream.getvalue())


def logout(request):
    """注销账户"""
    # 清除sessin数据
    request.session.clear()
    return redirect("/login/")
