from django.db import models
from imagekit.models import ProcessedImageField
# Create your models here.


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
