from django.shortcuts import render, redirect, HttpResponse



def demo(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    flag = False
    if username == 'rocks' and password == '123':
        flag = True
        # return redirect('/index/')
        import json
        return HttpResponse(json.dumps(flag))
    else:
        import json
        return HttpResponse(json.dumps(flag))