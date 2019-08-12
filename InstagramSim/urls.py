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

from Insta.views import SignUp
# 因为SignUp是对于Project层面而言的，所以不是在Insta App里的Views创建
# a better practice is to 创建一个 User App，然后把login, logout, signup, change profile都放在
# User App 里 instead of in Insta app, but now for Alpha version stick with Insta

urlpatterns = [
    path('admin/', admin.site.urls),
    # 如果传进来的app路径是以'Insta'开头的，那就去找/include这个app的url文件 Insta/'urls.py'
    path('Insta/', include('Insta.urls')),
    # 如果传进来的App是auth, 那就交给django自己提供的authorization feature app处理, which is installed in settings.py when I 'python startproject'
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup/', SignUp.as_view(), name='signup'),
]
