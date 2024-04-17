from django.db import models


class Department(models.Model):
    """部门"""
    title = models.CharField(max_length=32, verbose_name='职位')

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户"""
    username = models.CharField(max_length=12, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='账户余额')
    create_time = models.DateField(verbose_name='入职时间')
    # 实际上数据库中属性名 depart_id
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE, verbose_name='所属部门')
    gender_choice = {
        (1, "男"),
        (2, "女")
    }
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)


class PrettyNum(models.Model):
    """靓号"""
    mobile = models.CharField(max_length=11, verbose_name='靓号')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    level_choice = {
        (1, "初级"),
        (2, "中级"),
        (3, "高级"),
        (4, "特级")
    }
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choice, default=1)
    state_choice = {
        (1, "未占用"),
        (2, "已占用")
    }
    state = models.SmallIntegerField(verbose_name='状态', choices=state_choice, default=1)


class Admin(models.Model):
    """管理员"""
    name = models.CharField(max_length=12, verbose_name='用户名')
    pwd = models.CharField(max_length=64, verbose_name='密码')

    def __str__(self):
        return self.name


class Task(models.Model):
    """任务"""
    title = models.CharField(max_length=64, verbose_name='标题')
    detail = models.TextField(verbose_name='详细信息')
    level_choices = {
        (1, "紧急"),
        (2, "普通"),
        (3, "临时"),
    }
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=2)
    # 数据库中实际字段名 user_t_id
    user_t = models.ForeignKey(to="Admin", on_delete=models.CASCADE, verbose_name='负责人')


class Order(models.Model):
    """订单表"""
    order_id = models.CharField(verbose_name="订单号", max_length=64)
    name = models.CharField(max_length=32, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    status_choices = {
        (1, "待支付"),
        (2, "已支付"),
    }
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")
    # 数据库中字段名 user_id
    user_o = models.ForeignKey(to='Admin', on_delete=models.CASCADE, verbose_name='管理员')


class Data1(models.Model):
    """存储基于Form实现的文件上传数据"""
    name = models.CharField(max_length=32, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    # 存储的是图片文件路径---> CharField
    imgurl = models.CharField(verbose_name='头像', max_length=128)


class City(models.Model):
    """存储基于ModelForm实现的文件上传数据"""
    name = models.CharField(max_length=32, verbose_name='名称')
    count = models.IntegerField(verbose_name='人口')
    # 本质上仍是CharField 但是写成FileField可以通过ModelForm进行简化操作
    # upload_to='city/' 指明文件上传到media下的哪个目录
    imgurl = models.FileField(verbose_name='图片', max_length=128, upload_to='city/')
