from django.urls import path
# 相对导入
from .views import depart, upload

# 文件上传
urlpatterns = [
    path('list/', upload.upload_list),
    path('multi/', depart.depart_multi),
    path('form1/', upload.upload_form1),
    path('form2/', upload.upload_form2),
    path('modelform/', upload.upload_modelform),
]
