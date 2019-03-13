# @Time    : 2019/2/9 14:37
# @Author  : liyonghan
# @Email   : 772632967@qq.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r'get_comment_tree/(\d+)$',views.get_comment_tree),
    url(r'poll/',views.poll),
    url(r'comment/',views.comment),
    url(r'(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<keyword>.*)/$',views.home),
    url(r'(?P<username>\w+)/article/(?P<pk>\d+)/$',views.article_detail),
    url(r'(?P<username>\w+)/$',views.home),
    #文章详情
]