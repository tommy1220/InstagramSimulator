# 这里的urls.py是管理这个Insta app的 URL 信息，这和global的Project粒的urls.py意思一样
# 可以在global的Project粒的urls.py里面包括这个app的这个urls.py

"""InstagramSim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Insta.views import HelloWorld  # 1. 从Insta这个app里面import HelloWord这个View

urlpatterns = [
    # 这里是app里的url, 那应该用fuction views, class-based views, or including another URLconf?
    # 因为 class HelloWorld是一个class-based views, 所以用这个
    # 2.当传入''作为默认路径时，会调HelloWord这个View的as_View(), 因为as_View()方法继承里TemplateView，可以直接用,把'test.html' render出来
    path('', HelloWorld.as_view(), name='helloworld')
]
