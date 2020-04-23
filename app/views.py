from django.http import HttpResponse
from django.shortcuts import render,redirect
from app.libs.identity_check import check
from app.libs.initJson import initJson
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from app.models import *


def get_current_user(request):
    user = Users.objects.get(id=2)
    return user



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
    try:
        key = request.GET["s"]
        q = Question.objects.filter(title__contains=key)
        print(key)
    except:
        q = Question.objects.all()
    q = q.order_by("-top")
    paginator = Paginator(q,15)
    page = request.GET.get("page")
    try:
        page = int(page)
        q = paginator.page(page)
    except:
        q = paginator.page(1)
        page = 1
    question = q
    print(page)
    return render(request,"questions.html",{"q":q,"paginator":paginator,"page":page})


def detail(request,id):
    if request.method == "POST":
        user = get_current_user(request)
        content = request.POST.get("content")
        if content and content != "":
            Answer.objects.create(users=user,content=content,question_id=int(id))
    question = Question.objects.get(id=int(id))
    return render(request, "detail.html", {"question":question})


def add_question(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        bonus = request.POST.get("bonus")
        user = get_current_user(request)
        Question.objects.create(users=user, title=title, content=content, bonus=bonus)
        for i in range(100):
            title = "超级问题" + str(i)
            content = "批量添加得内容"+ str(i)
            Question.objects.create(users=user, title=title, content=content, bonus=bonus)
        return redirect("/index/")
    return render(request,"add_question.html")

#
# def add_answer(request):
#     if request.method == "POST":
#         pass
#     else:
#         errJson = initJson(success=False)
#         errJson['detail'] = "该账户已存在"
#         return HttpResponse(json.dumps(errJson), content_type="application/json")