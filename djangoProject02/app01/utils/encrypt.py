from django.conf import settings

import hashlib


# encrypt v.将...译成密码

def md5(data_string):
    # 加言
    # salt = "xxxxxxx"
    # obj = hashlib.md5(salt.encode("utf-8"))
    # obj.update(data_string.encode('utf-8'))
    # return obj.hexdigest()

    # 用django自带的言
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
