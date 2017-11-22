import json
from django.shortcuts import render, redirect, HttpResponse
from csdn.forms import  *
from blog.geetest import GeetestLib
from csdn import forms
from django.contrib import auth
from csdn.demo import demo

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


# Create your views here.


# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     print(username)
#     print(password)
#     flag = False
#     if username == 'rocks' and password == '123':
#         flag = True
#         # return redirect('/index/')
#         import json
#         return HttpResponse(json.dumps(flag))
#     else:
#         import json
#         return HttpResponse(json.dumps(flag))

def login(request):

    a = demo(request)
    return a


def regist(request):

    if request.is_ajax():  #如果是ajax请求
        form_obj=forms.RegForm(request,request.POST)  #获取数据

        regResponse={"user":None,"errorsList":None}
        if form_obj.is_valid():    #如果符合条件，取数据

            username=form_obj.cleaned_data["username"]
            password=form_obj.cleaned_data["password"]
            email=form_obj.cleaned_data.get("email")
            avatar_img=request.FILES.get("avatar_img")  #文件取法
            #写入数据，用原生user要写成creat_user
            user_obj=models.UserInfo.objects.create_user(username=username,password=password,email=email,avatar=avatar_img,nickname=username)
            print(user_obj.avatar,"......")
            regResponse["user"]=user_obj.username

        else:
            regResponse["errorsList"]=form_obj.errors
        import json
        return HttpResponse(json.dumps(regResponse))


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
    if request.method == 'GET':
        return render(request, 'index.html')
