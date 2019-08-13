from django.contrib import admin
from Insta.models import Post, Post2, InstaUser

# Register your models here.

# 这里添加哪些model是应该可以在admin上显示
admin.site.register(Post)
admin.site.register(Post2)
admin.site.register(InstaUser)
# notes: 在某milestone之前我使用的都是django.auth自带的user, 但是自从我换成自定义的
# customUser之后，之前的admin一只在用的user会出问题。但是因为django自带的user不能解决这个
# 统一问题，所以只能暴力删除db。 最好的办法就是在design的时候做好决定, 或者一开始就使用自定义CustomUser。
# that's why django sugeested using CustomUser i guess
# 但是不可能避免在自定义User的基础上，之后还会做改动，这时候就需要修改DB来解决，但是没必要删除DB因为已经使用了自定义的CustomUser
