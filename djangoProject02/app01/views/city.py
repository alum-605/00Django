from django.shortcuts import render, redirect
from app01.models import City

"""城市管理"""


def city_list(request):
    """城市列表"""
    models = City.objects.all()
    return render(request, "city_list.html", {"models": models})