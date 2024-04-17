from django import forms


class MyBootStrap:
    bootstrap_exclude_fields = []

    # 重写构造方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到每一个插件添加class="form-control"样式
        for name, field in self.fields.items():
            # 单独对某一个字段设置
            # if name == "password"
            #   continue
            # field.widget.attrs = {"class": "form-control", "placeholder": field.label}

            # 跳过想要不设置统一样式的字段
            if name in self.bootstrap_exclude_fields:
                continue

            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(MyBootStrap, forms.ModelForm):
    # 还可以在内部进行差异化
    pass


class BootStrapForm(MyBootStrap, forms.Form):
    pass
