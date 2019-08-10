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

# 1. 从Insta这个app里面import HelloWord这个View 2. and PostsView 3.and PostDetailView
from Insta.views import HelloWorld, PostsView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # 这里是app里的url, 那应该用fuction views, class-based views, or including another URLconf?
    # 因为 class HelloWorld是一个class-based views, 所以用这个
    # 当传入''作为默认路径时，会调HelloWord这个View的as_View(), 因为as_View()方法继承里TemplateView，可以直接用,把'test.html' render出来
    path('', HelloWorld.as_view(), name='Bello Papagena'),
    # 当传入post/作为路径时，会调PostsView这个View的as_View(), eg. http://localhost:8000/Insta/posts/
    path('posts/', PostsView.as_view(), name='posts'),
    # 如果传进来的path/并且加一个int，那我就用这个int as 'Post'这个model的primary key(ID),然后之后render在html里
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # 如果传来的path带着的post/new/ 那就调用PostCreatView
    path('post/new/', PostCreateView.as_view(), name='make_post'),
    # 同post_detail 如果有人传进来post/update/ID 那就可以update
    path('post/update/<int:pk>', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),
]
