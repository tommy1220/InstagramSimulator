# 自定义的一个.py, 存在的意义就是，当我想用自定义的user时，那么就不能再用Django自带的
# user view 和 UserCreationForm 之类的但凡是和Django自带user相关的东西了。
# 因为 UserCreationForm 是一个用于创建用户的Form, 我自己要重新定义的话最好就把它和别的forms都丢在一个forms.py文件里
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

# forms defined here handles user inputs


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InstaUser  # Model是自定义的InstaUser
        # 'username', 'email' were predefined by AbstractUser view by django
        fields = ('username', 'email', 'profile_pic')
