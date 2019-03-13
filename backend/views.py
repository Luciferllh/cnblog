from django.shortcuts import render,HttpResponse
from cnblog import settings
import os,json
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from blog.models import *
# Create your views here.

@login_required()
def add_article(request):

    if request.method == 'POST':
        title=request.POST.get('title')
        article_content=request.POST.get('article_content')
        user = request.user
        bs = BeautifulSoup(article_content,'html.parser')

        #过滤非法标签
        for tag in bs.find_all():
            print(tag.name)
            if tag.name=='script':
                tag.decompose()
        article_content = str(bs)
        print(article_content)
        desc=bs.text[0:150]
        article_obj=Article.objects.create(user=user,title=title,desc=desc)
        print(article_obj)
        ArticleDetail.objects.create(content=article_content,article=article_obj)
        return HttpResponse('添加成功')
    return render(request,'add_article.html')



def upload_article(request):
    print(request.FILES)
    obj=request.FILES.get('upload_img')
    print(obj.name,obj.size)
    path=os.path.join(settings.MEDIA_ROOT,'add_article_img',obj.name)

    with open(path,'wb') as f:
        for line in obj:
            f.write(line)
    res={'error':0,
         'url':'/media/add_article_img/{}'.format(obj.name)}
    print(res)
    return HttpResponse(json.dumps(res))