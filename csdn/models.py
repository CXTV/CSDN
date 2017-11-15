from django.db import models


# Create your models here.
class Artical(models.Model):
    '''
    文章
    '''
    title = models.CharField(max_length=64, verbose_name='标题')
    creat_time = models.DateTimeField(auto_now=True, verbose_name='创建日期')
    summary = models.CharField(max_length=128, verbose_name='摘要')




class Poll(models.Model):
    '''
    点赞
    '''
    is_positive = models.BooleanField(default=True, verbose_name='点赞或踩')
    poll_number = models.IntegerField(verbose_name='点赞次数')


class Content(models.Model):
    '''
    文章内容
    '''
    content = models.TextField(verbose_name='文章内容')


class Comment(models.Model):
    '''
    评论
    '''
    comment = models.CharField(max_length=128, verbose_name='评论')
    comment_time = models.TimeField(auto_now_add=True, verbose_name='评论时间')


class CommentPoll(models.Model):
    '''
    评论点赞
    '''
    is_positive = models.BooleanField(default=True, verbose_name='评论点赞')
    number = models.IntegerField(verbose_name='次数')


class Classify(models.Model):
    '''
    文章分类
    '''
    Classify_name = models.CharField(verbose_name='分类')


class Tag(models.Model):
    '''
    标签
    '''
    tag_name = models.CharField(verbose_name='标签')


class User(models.Model):
    '''
    用户表
    '''
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')


class UserInfo(models.Model):
    '''
    用户详情
    '''
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    age = models.CharField(max_length=32, verbose_name='年龄')
    sex = models.CharField(max_length=32, verbose_name='性别')
    email = models.CharField(max_length=64, verbose_name='邮箱地址')
    job = models.CharField(max_length=32, verbose_name='工作')
    education = models.CharField(max_length=32, verbose_name='教育')
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    photo = models.ImageField(verbose_name='头像')


class Mail(models.Model):
    '''
    站内信
    '''
    mail = models.CharField(max_length=128, verbose_name='站内信')


class Blog(models.Model):
    '''
    站点
    '''
    blogname = models.CharField(max_length=32, verbose_name='站点名')
    url = models.CharField(max_length=32, verbose_name='站点路径')
