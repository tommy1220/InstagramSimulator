from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse  # urls库里的reverse函数可以帮助get_absolute_url
from django.contrib.auth.models import AbstractUser


class Post(models.Model):  # 所有model的class都要继承models
    # 定义里一个title field, 可以是blank，也可以是null
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


class Post2(models.Model):  # 所有model的class都要继承models
    # 定义里一个title field, 可以是blank，也可以是null
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(  # 定义的第二个field 是 ProcessImageField(imported from imagekit)第三方library里的类型
        upload_to='static/images/posts',  # 图片应该上传到哪里
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )


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
