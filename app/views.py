from django.http import HttpResponse
from django.shortcuts import render,redirect
from app.libs.identity_check import check
from app.libs.initJson import initJson
import json
# Create your views here.

#拦截器 用于检测用户是否登录
from app.models import Users


def login_need(func):
    def wrapper(req,*arg,**kwargs):
        if not req.session.get('username'):
            return redirect("/login_register_page/")
        return func(req,*arg,**kwargs)
    return wrapper


def login_register_page(request):
    return render(request, "login_register.html")


#用户登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        user = Users.objects.filter(username=username,password=passwd)
        errJson = initJson(success=False)
        if user:
            if user.first().status != "T":
                errJson['detail'] = "禁止登陆！"
                return HttpResponse(json.dumps(errJson), content_type="application/json")
            request.session["username"] = username
            return HttpResponse(json.dumps(initJson()), content_type="application/json")
        else:
            errJson['detail'] = "账号或者密码错误"
            return HttpResponse(json.dumps(errJson), content_type="application/json")
    else:
        return redirect("/login_register_page/")


#用户注册
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        user = Users.objects.filter(username=username)
        if user:
            errJson = initJson(success=False)
            errJson['detail'] = "该账户已存在"
            return HttpResponse(json.dumps(errJson), content_type="application/json")
        else:
            Users.objects.create(username=username,password=passwd).save()
            return HttpResponse(json.dumps(initJson()), content_type="application/json")
    else:
        return redirect("/login_register_page/")


#帖子主页
def index(request):
    return render(request,"index.html")


def questions(request):
    return render(request,"questions.html")


def detail(request):
    test=  "df"
    return render(request, "detail.html", {"test":test})


def add_question(request):
    return render(request,"add_question.html")