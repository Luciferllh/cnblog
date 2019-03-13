# @Time    : 2019/2/9 14:37
# @Author  : liyonghan
# @Email   : 772632967@qq.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from backend import views


urlpatterns = [
   url(r'add_article/$',views.add_article),
    url(r'^upload_article/$',views.upload_article)
]