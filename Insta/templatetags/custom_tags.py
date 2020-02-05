# The app should contain a templatetags directory, at the same level as models.py, 
# views.py, etc. If this doesn’t already exist, create it - don’t forget the __init__.py 
# file to ensure the directory is treated as a Python package.
import re

from django import template
from django.urls import NoReverseMatch, reverse
from Insta.models import Like


register = template.Library()

@register.simple_tag
def is_following(current_user, background_user):
    return background_user.get_followers().filter(creator=current_user).exists()

@register.simple_tag
def has_user_liked_post(post, user):
    try:
        # 因为like，在models.py里定义过了，是个向外foreign key的一个model, 并且一个like关系只能存在
        # 一个user点赞一个post, 所以如果这个关系满足的话，返回小爱心；否则返回小空心
        like = Like.objects.get(post=post, user=user)
        return "fa-heart"
    except:
        return "fa-heart-o"

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''