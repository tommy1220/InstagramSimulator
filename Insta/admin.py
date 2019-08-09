from django.contrib import admin
from Insta.models import Post, Post2

# Register your models here.

# 这里添加哪些model是应该可以在admin上显示
admin.site.register(Post)
admin.site.register(Post2)
