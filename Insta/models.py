# pylint: disable=no-member
from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse  # urls库里的reverse函数可以帮助get_absolute_url
from django.contrib.auth.models import AbstractUser

# 为了可以自定义user类能干嘛，而不是仅仅局限于django自带的user views, 那么就可以继承一个AbstractUser
# 但是自从创建里InstaUser之后，在此之前所用的Django.auth的user view就不能被使用里。
# 这里的programming code虽然定义好了新的user, 但是数据库并不知道，所以需要python manage.py makemigration, and migrate一下
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(  # 定义的第二个field 是 ProcessImageField(imported from imagekit)第三方library里的类型
        upload_to='static/images/profiles',  # 图片应该上传到哪里
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )


class Post(models.Model):  # 所有model的class都要继承models
    # 因为一个Post肯定是一个用户发的，所以向外指向一个InstaUser
    author = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="my_posts"
    )
    # 可以利用my_posts来找到一个user发的全部的posts
    # 定义里一个title field, 可以是blank，也可以是null
    # 另外，现在Post有了多一个field叫author, 在make migrations的时候会出问题：
    # can't do that (the database needs something to populate existing rows)
    # 但是一个author (author is a user) 却又是很大很复杂的object, 不能简简单单地去把一个user给设置一个null默认值
    # 所以unfortunately在增加了author这个field后，又要去暴力清空一次数据库
    # again as stated at the end of admin.py, 一开始就考虑好各个models之间的关系，一开始设计好了，之后才不用
    # 老是去暴力删除数据库, but again 这里还是需要暴力删除： 
    # rm db.sqlite3  
    # under Insta/ directory's migraitons/, 因为之前一直在用的是没有 author 这个field的migrations, 所以也要删除他们
    # rm all the migrations file under migrations/   rm 0001_initial.py 002... only left with __init__.py
    # after than, python manage.py makemigrations
    #   Insta/migrations/0001_initial.py
    #     - Create model InstaUser
    #     - Create model Post
    #     - Create model Like
    # finally,  python manage.py createsuperuser  to make the superuser and..
    # python manage.py migrate  to migrate the new Post model to database
    # check it up in http://localhost:8000/admin/Insta/post/ by loggin in with superuser, should have new models
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(  # 定义的第二个field 是 ProcessImageField(imported from imagekit)第三方library里的类型
        upload_to='static/images/posts',  # 图片应该上传到哪里
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )

    # 原本post_create.html里点击save图片会报错：No URL to redirect to.
    # Either provide a url or define a get_absolute_url method on the Model.
    # 那我就defind一个get_ab_url method on the model咯
    # 这个函数，当有人新建里一个Post以后，就会被调用，并且它里面的　reverse
    # eg. return reverse("BelloPapagena") ...
    # www.amazon.com/basketballs -> some page;
    # reverse则是将 "Bello Papagena" -> 对应的是哪个网址 -> www.amazon.com/basketballs -> some page 找到这个界面
    # 在urls.py发现path('', HelloWorld.as_view(), name='Bello Papagena'), 所以通过 "Bello Papagena"可以找到那个界面
    # 那么实际上，我希望save一个图片以后可以转到post_detail里
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # 但是这里还需要传入一个 primary key as the args. 所以我可以传入一个list of Strings, self.id就是当前Post object的ID 传入进来当作PK

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    # 可是当删除一个Post的object后，又会报错: No URL to rediredt to.
    # 这是因为，与create/update不同当是，当create/update一个object点击save/update button后，这个model会invoke
    # get_absolute_url回到通过“post_detail”回到那个path里，但是这里delete了以后都没有object了，怎么办？
    # Django自己提供了一个success_url的办法，当成功delete, 跳转到指定的success_url里去

    def get_like_count(self):
        return self.likes.count()
        #post1.likes -> (like1, like2) , then count is 2


# 上面有了Post和InstaUser，但是这两者之间没有联系，所以需要新建立一个model来使得user和user发的posts有联系
# 我要知道哪一个用户点赞了哪个 POST, 所以Like这个model是一个关系型的，类似database里的foreign key,
# 它表示这个POST是一个指向外部的foreign key。 还有，当某个自己点赞的post被删除后，这个点赞关系也要删除
class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # 当某个自己点赞的post被删除后，这个点赞关系也要删除
        related_name='likes')
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    # 每一个‘Like’ object都向外指向了一个 Post model object 和一个 InstaUser model object
    # 当InstaUser Tommy and Mingjun 都去点赞了 post1, 会生成两个 'Like' object
    # like1 -> Tommy likes post 1
    # like2 -> Mingjun likes post 1
    # 在like1和like2这两个object身上我可以利用我自己定义的related_name 'likes'
    # 找到所有点赞了这个post 1的foreign key objects: 如下
    # post1.likes -> (like1, like2)  Tommy.likes -> (like1)  Mingjun.likes -> (like2)

    class Meta:
        unique_together = ("post", "user")
        # 一个InstaUser只能给一个Post点一次赞：对于同一个InstaUser和同一个Post这个pair,只能存在一次

    # 在admin里面用一个makes sense的sentence表示出来， 而不是 'Like object(1)'
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes the post with the title:  ' + self.post.title

# class Comment(models.Model):
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments',)
#     user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=100)
#     posted_on = models.DateTimeField(auto_now_add=True, editable=False)

#     def __str__(self):
#         return self.comment




# class Post2(models.Model):  # 所有model的class都要继承models
#     # 定义里一个title field, 可以是blank，也可以是null
#     title = models.TextField(blank=True, null=True)
#     image = ProcessedImageField(  # 定义的第二个field 是 ProcessImageField(imported from imagekit)第三方library里的类型
#         upload_to='static/images/posts',  # 图片应该上传到哪里
#         format='JPEG',
#         options={'quality': 100},
#         blank=True,
#         null=True
#     )