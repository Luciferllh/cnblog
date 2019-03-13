"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
from django.views.static import serve
from cnblog import settings
from blog import urls as blog_urls
from backend import urls as backend_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^get_vail_img/', views.get_vail_img),
    url(r'^index/',views.index),
    url(r'^register/',views.register),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

    #极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register',views.get_geetest),

    #
    url(r'^blog/',include(blog_urls)),

    url(r'^test/',views.test),

    #后台管理
    url(r'backend/',include(backend_urls))
]
