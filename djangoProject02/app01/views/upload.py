import os
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings

from app01.models import Data1, City
from app01.utils.bootstrapdodelform import BootStrapForm, BootStrapModelForm


def upload_list(request):
    """基本文件上传"""
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    # POST请求体中除了文件之外的数据
    print(request.POST)
    # <QueryDict: {
    # 'csrfmiddlewaretoken': ['Zw0Z4witRuVxMuhDS8ycVIoTLonnOTnFiANOrJ9pDl7hXlbCmTcPCjUZjMNQwJPF'], 'photo': ['alum']
    #  }>
    print(request.FILES)
    # <MultiValueDict: {
    # 'photo_file-1': [<InMemoryUploadedFile: xxx.jpg (image/jpeg)>],
    # 'photo_file-2': [<InMemoryUploadedFile: 王际翔第二次软件测试作业.wps (application/wpsoffice)>],
    # 'photo_file-3': [ < InMemoryUploadedFile: IMG_5599.JPG(image / jpeg) >]
    # }>

    file_obj1 = request.FILES.get('photo_file-1')
    file_obj2 = request.FILES.get('photo_file-2')
    file_obj3 = request.FILES.get('photo_file-3')
    # 文件名
    print(file_obj1.name)
    print(file_obj2.name)

    write_file1(file_obj1)
    write_file1(file_obj2)
    write_file1(file_obj3)
    return HttpResponse("上传成功")


def write_file1(fielobj):
    """写文件到static"""
    fname = fielobj.name
    # 文件存储路径："app01/static/img/{}".format(fname) 使用os拼接地址的原因：避免win和lunx对'/'的不同处理
    db_file_path = os.path.join("static", "img", fname)
    # static 应当只存放开发者使用的静态文件
    # 用户使用过程中上传的文件应当存储在其它制定文件夹内
    file_path = os.path.join("app01", db_file_path)

    # 以写的方式新打开一个文件
    f = open(file_path, 'wb')
    # 文件数据 分块上传和读取
    for chunk in fielobj:
        f.write(chunk)
    f.close()
    # 数据库中写这个 不加app01是为了好和localhost拼接 访问图片
    # http://localhost:8000/static/img/xxx.jpg
    # 但是实际存储位置是file_path
    return db_file_path


class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form1(request):
    title = "Form文件上传至static"
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})
    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'name': 'Alum', 'age': 16, 'img': <InMemoryUploadedFile: xxx.jpg (image/jpeg)>}
        # 1.处理数据
        # 2.处理文件
        # 2.1读取图片内容，写入文件夹中 并读取文件路径
        img_obj = form.cleaned_data.get("img")
        # 2.2将路径存储到数据库
        Data1.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            imgurl=write_file1(img_obj)
        )
        return HttpResponse('上传成功')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


def upload_form2(request):
    title = "Form文件上传至media"
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})
    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        img_obj = form.cleaned_data.get("img")
        # media_path = os.path.join(settings.MEDIA_ROOT, img_obj.name)
        # 绝对路径 /Users/alum/Documents/Code/Python/Django/djangoProject02/media/xxx.jpg
        media_path = os.path.join("media", img_obj.name)

        f = open(media_path, "wb")
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()

        Data1.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            imgurl=media_path
        )
        return HttpResponse('上传成功')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['imgurl']

    class Meta:
        model = City
        fields = '__all__'


def upload_modelform(request):
    title = "ModelForm文件上传(配置好默认至Media)"
    if request.method == 'GET':
        form = UploadModelForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # !!!!!!!与Form区别
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


