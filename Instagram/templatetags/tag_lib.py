from django import template
from Instagram.models import *
register = template.Library()

@register.filter()
def to_int(value):
    return int(value)
@register.filter()
def liked(likes,id):
    post =POST.objects.filter(id=id)
    return post
@register.filter()
def is_liked_curr(like,user):
    for i in like:
        for j in i.likes.all():
            if j.username== user:
                print(j.username)
                return True
        else:
            return False