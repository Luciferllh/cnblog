# @Time    : 2019/2/9 22:04
# @Author  : liyonghan
# @Email   : 772632967@qq.com
# @File    : my_tags.py
# @Software: PyCharm

from  django import template
from  blog.models import *
from django.db.models import Count

register= template.Library()


@register.inclusion_tag('blog/left_menu.html')
def get_left_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = Category.objects.filter(blog=blog).annotate(c=Count('article'))
    tag_list = Tag.objects.filter(blog=blog).annotate(d=Count('articletotag'))
    archive_list = Article.objects.filter(user=user).extra(
        select={'archive_ym': "date_format(create_time,'%%Y-%%m')"}
    ).values('archive_ym').annotate(e=Count('nid')).values('archive_ym', 'e')
    return {'category_list':category_list,'tag_list':tag_list,'archive_list':archive_list,'username':username}