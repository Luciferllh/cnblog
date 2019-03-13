from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import auth
from django import forms
from blog.models import *
from geetest import GeetestLib
from django.db.models  import F
import json
from django.db.models import Count
from django.forms import widgets
from django.contrib.auth.decorators import login_required
# Create your views here.
# def login(request):
#     if request.is_ajax():
#         user=request.POST.get('user')
#         pwd=request.POST.get('pwd')
#         valid_code=request.POST.get('valid_code')
#         res={"state":None,"msg":False}
#         valid_str=request.session.get("valid_str")
#         if valid_code.upper() == valid_str.upper():
#             user=auth.authenticate(username=user,password=pwd)
#             if user:
#                 res['state']=True
#                 auth.login(request,user)
#             else:
#                 res['msg']='用户名或密码错误'
#         else:
#             res["msg"]="验证码错误"
#         return JsonResponse(res)
#     return render(request,'login.html')

#使用滑动验证
def login(request):
    if request.is_ajax():
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')

        #滑动验证相关参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)


        res={"state":None,"msg":False}

        if result:
            user=auth.authenticate(username=user,password=pwd)
            if user:
                res['state']=True
                auth.login(request,user)
            else:
                res['msg']='用户名或密码错误'
        else:
            res["msg"]="验证码错误"
        return JsonResponse(res)
    return render(request, 'blog/login2.html')


def logout(request):
    auth.logout(request)
    return redirect('/login/')

def index(request):
    # if not request.user.username:
    #     return redirect('/login/')
    article_list=Article.objects.all()
    return render(request, 'blog/index.html', {'article_list':article_list})

def get_vail_img(request):
    # with open('avatar.png','rb') as f:
    #     data=f.read()


    from PIL import Image,ImageDraw,ImageFont
    import random
    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    image=Image.new('RGB',(250,32),get_random_color())
    draw=ImageDraw.Draw(image)
    font=ImageFont.truetype('static/bmyy.ttf',size=28)

    #生成随机字符
    temp=[]
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_low_alpha=chr(random.randint(97,122))
        random_upper_alpha=chr(random.randint(65,90))
        random_char=random.choice([random_num,random_low_alpha,random_upper_alpha])
        draw.text((15+i*50,0),random_char,get_random_color(),font=font)
        temp.append(random_char)
    # 图片中的噪点噪线
    # width=250
    # height=32
    #
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,x2,y1,y2),fill=get_random_color())
    #
    # for i in range(40):
    #     draw.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    #     x= random.randint(0,width)
    #     y= random.randint(0,height)
    #     draw.arc((x,y,x+4,y+4),0,90,fill=get_random_color())
    valid_str=''.join(temp)

    #将验证码数据存于session中
    request.session["valid_str"]=valid_str

    #内存对象
    from io import BytesIO
    f=BytesIO()
    image.save(f, 'png')
    data=f.getvalue()
    f.close()

    #硬盘对象
    # with open('valid_code.png','wb') as f :
    #     image.save(f,'png')
    # with open('valid_code.png','rb') as f :
    #     data=f.read()
    return HttpResponse(data)



class RegForm(forms.Form):
    user = forms.CharField(max_length=24,
                           label='用户名',
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(min_length=8,
                          label='密码',
                          widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
                          )
    repeat_pwd = forms.CharField(min_length=8,
                                 label='确认密码',
                                 widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
                                 )
    email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'class':'form-control'}))

    def clean_user(self):
        val=self.cleaned_data.get('user')

        ret=UserInfo.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise forms.ValidationError('该用户已存在')

    def clean(self):
        pwd=self.cleaned_data.get('pwd')
        re_pwd=self.cleaned_data.get('repeat_pwd')
        if pwd!=re_pwd:
            raise forms.ValidationError('两次密码不一致')
            # raise ValueError('两次密码不一致')
        return self.cleaned_data

def register(request):
    if request.method == 'POST':
        res={'user':None,'error_dict':None}
        form=RegForm(request.POST)
        print(form)
        if form.is_valid():
            print(form.cleaned_data)
            print(request.FILES)
            user=form.cleaned_data.get('user')
            pwd=form.cleaned_data.get('pwd')
            email=form.cleaned_data.get('email')
            avatar=request.FILES.get('avatar')
            if avatar:
                user=UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            res['user']=user.username
        else:
            res['error_dict']=form.errors
        return JsonResponse(res)
    form = RegForm()
    return render(request, 'blog/register.html', locals())


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
#处理极验 获取验证码
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


#个人博客主页
def home(request,username,**kwargs):
    print(username)
    print("关键字",kwargs)
    print('华丽的分割线'.center(50,'*'))
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    blog = user.blog
    if kwargs:
        condition=kwargs.get('condition')
        keyword=kwargs.get('keyword')
        if condition == 'category':
            article_list = Article.objects.filter(user=user).filter(category__title=keyword)
        elif condition == 'tag':
            article_list = Article.objects.filter(user=user).filter(tag__title=keyword)
        elif condition == 'archive':
            year,month=keyword.split('-')
            print(year,month)
            article_list = Article.objects.filter(user=user).filter(create_time__month=month,create_time__year=year)
            print(article_list)
    else:
        article_list=Article.objects.filter(user=user)

    return render(request, 'blog/home.html', {'blog':blog,
                                       'article_list':article_list,
                                       'username':username})


def article_detail(request,username,pk):
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    article_obj= Article.objects.filter(pk=pk).first()
    comment_list=Comment.objects.filter(article_id=pk)
    blog=user.blog
    print(article_obj)
    return render(request, 'blog/article.html', {'article_obj':article_obj,
                                          'blog':blog,
                                          'username':username,
                                          'comment_list':comment_list
                                                 })


def test(request):
    user=UserInfo.objects.filter(username='lucifer').first()
    tag= Tag.objects.filter(title='django')
    article_list=Article.objects.filter(tag=tag).filter(user=user)
    # article_list=Article.objects.filter(user=user).filter(tag__title='django')
    print(article_list)
    return HttpResponse('hello')

def poll(request):
    print(request.POST)
    is_up=json.loads(request.POST.get('is_up'))
    print('is_up',is_up)
    article_id=request.POST.get('article_id')
    user_id=request.user.pk
    res={'state':True}
    try:
        ArticleUpDown.objects.create(is_up=is_up,article_id=article_id,user_id=user_id)
        if is_up:
            Article.objects.filter(pk=article_id).update(up_count=F('up_count')+1)
        else:
            Article.objects.filter(pk=article_id).update(down_count=F('down_count')+1)
    except  Exception as e:
        res['state']=False
        res['first_action']=ArticleUpDown.objects.filter(article_id=article_id,user_id=user_id).first().is_up
        print('first',res['first_action'])
    return JsonResponse(res)

def comment(request):
    print(request.POST)
    pid=request.POST.get('pid')
    article_id=request.POST.get('article_id')
    content=request.POST.get('content')
    user_pk=request.user.pk
    response={}
    if not pid:
        comment_obj=Comment.objects.create(article_id=article_id,content=content,user_id=user_pk)
    else:
        comment_obj = Comment.objects.create(article_id=article_id, content=content, user_id=user_pk,parent_comment_id=pid)
    response['create_time']=comment_obj.create_time.strftime('%Y-%m-%d %X')
    print(type(comment_obj.create_time))
    print(type(response['create_time']))
    response['content']=comment_obj.content
    response['user']=comment_obj.user.username
    print(response)

    return JsonResponse(response)


def get_comment_tree(request,id):
    ret=list(Comment.objects.filter(article_id=id).values('pk','content','parent_comment_id','user__username'))
    print(ret)
    return JsonResponse(ret,safe=False)