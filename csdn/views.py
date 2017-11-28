import json
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, HttpResponse
from csdn.forms import *
from blog.geetest import GeetestLib
from csdn import forms
from django.contrib import auth

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


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


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def mobilegetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(mobile_geetest_id, mobile_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def pcvalidate(request):
    if request.method == "POST":
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
        result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
        return HttpResponse(result)
    return HttpResponse("error")


def pcajax_validate(request):
    if request.method == "POST":
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
        result = {"status": "success"} if result else {"status": "fail"}
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")


def index(request):
    artical_list = models.Article.objects.all()

    return render(request, 'index.html', {'artical_list': artical_list})


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
                   'category_list': category_list, 'tag_list': tag_list, 'date_list': date_list,'current_blog':current_blog})


def articleDetail(request, username,article_id):
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

    article_obj=models.Article.objects.filter(nid=article_id).first()

    return render(request, 'articleDetail.html',locals())


def poll(request):

    return HttpResponse(json.dumps())