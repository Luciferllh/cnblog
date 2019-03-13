from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11)
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.jpg')
    creat_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    blog = models.OneToOneField(to='Blog', to_field='nid', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name ='用户'
        verbose_name_plural=verbose_name


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='个人博客标题')
    site = models.CharField(max_length=32, verbose_name='个人博客后缀', unique=True)
    theme = models.CharField(max_length=32, verbose_name='个人博客主题')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name ='blog站点'
        verbose_name_plural=verbose_name

class Category(models.Model):
    """
    博客个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='分类标题')
    blog = models.ForeignKey(to='Blog', to_field='nid', verbose_name='所属博客')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标签名称')
    blog = models.ForeignKey(to='Blog', to_field='nid', verbose_name='所属博客')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    comment_count = models.IntegerField(verbose_name='评论数',default=0)
    up_count = models.IntegerField(verbose_name='点赞数',default=0)
    down_count = models.IntegerField(verbose_name='踩数',default=0)
    category = models.ForeignKey(to='Category', to_field='nid', null=True,verbose_name='分类')
    tag = models.ForeignKey(to='Tag', to_field='nid', null=True,verbose_name='标签')
    user = models.ForeignKey(to='UserInfo', to_field='nid', verbose_name='作者')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid')

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name


class ArticleToTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', verbose_name='文章')
    tag = models.ForeignKey(to='Tag', to_field='nid', verbose_name='标签')

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]
        verbose_name = '文章·标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        v = self.article.title + '--' + self.tag.title
        return v

class ArticleUpDown(models.Model):
    """
    点赞
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey('Article', null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user')
        ]
        verbose_name = '点赞系统'
        verbose_name_plural = verbose_name

class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo',to_field='nid', verbose_name='评论者')
    article = models.ForeignKey(to='Article',to_field='nid', verbose_name='评论文章')
    content = models.CharField(max_length=255,verbose_name='评论内容')
    create_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
    parent_comment = models.ForeignKey('self',null=True,blank=True)

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name