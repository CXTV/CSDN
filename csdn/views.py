import json
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, HttpResponse
from csdn.forms import *
from csdn import forms
from django.contrib import auth
from django.db.models import F


# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', )
    username = request.POST.get('username')
    password = request.POST.get('password')
    flag = False
    user = auth.authenticate(username=username, password=password)  # 判断用户名密码是否匹配
    if user:
        flag = True
        auth.login(request, user)  # 将用户名密码传入session
        # return redirect('/index/')
        return HttpResponse(json.dumps(flag))
    else:
        return HttpResponse(json.dumps(flag))


def regist(request):
    if request.is_ajax():
        form_obj = forms.RegForm(request, request.POST)

        regResponse = {"user": None, "errorsList": None}
        if form_obj.is_valid():

            username = form_obj.cleaned_data["username"]
            password = form_obj.cleaned_data["password"]
            email = form_obj.cleaned_data.get("email")
            avatar_img = request.FILES.get("avatar_img")

            user_obj = models.UserInfo.objects.create_user(username=username, password=password, email=email,
                                                           avatar=avatar_img, nickname=username)
            print(user_obj.avatar, "......")
            regResponse["user"] = user_obj.username

        else:
            regResponse["errorsList"] = form_obj.errors
        import json
        return HttpResponse(json.dumps(regResponse))

    form = forms.RegForm(request)
    return render(request, 'regist.html', {'form_obj': form})


def index(request, *args,**kwargs):
    print(kwargs)
    if kwargs:
        artical_list = models.Article.objects.filter(site_article_category__name =kwargs.get('site_articlecategory'))
    else:
        artical_list = models.Article.objects.all()

    cate_list = models.SiteCategory.objects.all()

    return render(request, 'index.html', {'artical_list': artical_list, 'cate_list': cate_list})


def logout(request):
    auth.logout(request)  # 清除session推出
    return redirect('/login')


def homeSite(request, username, **kwargs):  # 这里username传的是url里的有名分组?P
    # 查询当前用户
    current_user = models.UserInfo.objects.filter(username=username).first()
    current_blog = current_user.blog
    if not current_user:
        return render(request, 'notFound.html')

    # 查询当前文章内容
    artical_list = models.Article.objects.filter(user=current_user)  # 当前用户所有文章

    # 分组查询，聚合查询
    # 查询 当前用户的分类归档
    category_list = models.Category.objects.all().filter(blog=current_blog).annotate(
        c=Count("article__nid")).values_list("title", "c")
    # print(category_list)

    # 查询当前用户的标签归档
    tag_list = models.Tag.objects.all().filter(blog=current_blog).annotate(c=Count("article__nid")).values_list("title",
                                                                                                                "c")
    # print(tag_list)

    # 查询 当前用户的时间归档
    date_list = models.Article.objects.filter(user=current_user).extra(
        select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(
        Count("nid"))
    # print(date_list)

    # 跳转
    print(kwargs)
    # {'condition': 'category', 'para': 'rocks的mysql'} 传入的是字典形式
    if kwargs:
        if kwargs.get('condition') == 'category':
            artical_list = models.Article.objects.filter(user=current_user, category__title=kwargs.get("para"))  #
        elif kwargs.get("condition") == "tag":
            artical_list = models.Article.objects.filter(user=current_user, tags__title=kwargs.get("para"))
        elif kwargs.get("condition") == "date":
            year, month = kwargs.get("para").split("/")  # 去除/
            artical_list = models.Article.objects.filter(user=current_user, create_time__year=year,
                                                         create_time__month=month)

    return render(request, 'homeSite.html',
                  {'username': current_user, 'artical_list': artical_list, 'current_user': current_user,
                   'category_list': category_list, 'tag_list': tag_list, 'date_list': date_list,
                   'current_blog': current_blog})


def articleDetail(request, username, article_id):
    current_user = models.UserInfo.objects.filter(username=username).first()
    current_blog = current_user.blog
    if not current_user:
        return render(request, 'notFound.html')

    # 查询当前用户所有文章

    article_list = models.Article.objects.filter(user=current_user)

    # 查询 当前用户的分类归档
    from django.db.models import Count, Sum

    category_list = models.Category.objects.all().filter(blog=current_blog).annotate(
        c=Count("article__nid")).values_list("title", "c")
    print(category_list)  # <QuerySet [<Category: yuan的go>, <Category: yuan的java>]>

    # 查询当前用户的标签归档

    tag_list = models.Tag.objects.all().filter(blog=current_blog).annotate(c=Count("article__nid")).values_list("title",
                                                                                                                "c")
    print(tag_list)  # <QuerySet [('基础知识', 3), ('插件框架', 0), ('web开发', 1)]>

    # 查询当前用户的日期归档

    date_list = models.Article.objects.filter(user=current_user).extra(
        select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(
        Count("nid"))
    print(date_list)

    article_obj = models.Article.objects.filter(nid=article_id).first()

    return render(request, 'articleDetail.html', locals())


def poll(request):
    user_id = request.user.nid
    article_id = request.POST.get('article_id')
    pollResponse = {"state": True, "is_repeat": None}
    if models.ArticleUp.objects.filter(user_id=user_id, article_id=article_id):
        pollResponse["state"] = False
        pollResponse["is_repeat"] = True
    else:
        try:
            articleUp = models.ArticleUp.objects.create(user_id=user_id, article_id=article_id)
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)  # 点赞加一
        except:
            pollResponse["state"] = False
    return HttpResponse(json.dumps(pollResponse))


def demo(request):
    return render(request, 'demo.html')
