# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190208_0121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='articledetail',
            options={'verbose_name': '文章详情', 'verbose_name_plural': '文章详情'},
        ),
        migrations.AlterModelOptions(
            name='articletotag',
            options={'verbose_name': '文章·标签', 'verbose_name_plural': '文章·标签'},
        ),
        migrations.AlterModelOptions(
            name='articleupdown',
            options={'verbose_name': '点赞系统', 'verbose_name_plural': '点赞系统'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'blog站点', 'verbose_name_plural': 'blog站点'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AddField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='踩数'),
        ),
        migrations.AddField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment'),
        ),
    ]
