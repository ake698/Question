from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.libs.identity_check import login_need
from app.libs.initJson import initJson
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from app.models import *


def get_current_user(request):
    username = request.session["username"]
    user = Users.objects.get(username=username)
    return user


def login_register_page(request):
    return render(request, "login_register.html")


# 用户登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        user = Users.objects.filter(username=username, password=passwd)
        errJson = initJson(success=False)
        if user:
            if user.first().status != "T":
                errJson['detail'] = "禁止登陆！"
                return HttpResponse(json.dumps(errJson), content_type="application/json")
            request.session["username"] = username
            request.session["nickname"] = user.first().nickname
            return HttpResponse(json.dumps(initJson()), content_type="application/json")
        else:
            errJson['detail'] = "账号或者密码错误"
            return HttpResponse(json.dumps(errJson), content_type="application/json")
    else:
        return redirect("/login_register_page/")


# 用户注册
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
            user = Users.objects.create(username=username, password=passwd)
            user.nickname = "新用户" + str(user.id)
            user.save()
            return HttpResponse(json.dumps(initJson()), content_type="application/json")
    else:
        return redirect("/login_register_page/")


# 用户注销
@login_need
def logout(request):
    request.session.flush()
    response = HttpResponse("注销成功")
    response['Refresh'] = "2;/"
    return response


@login_need
# 帖子主页
def index(request):
    return render(request, "index.html")


@login_need
def questions(request):
    try:
        key = request.GET["s"]
        q = Question.objects.filter(title__contains=key)
    except:
        q = Question.objects.all()
    q = q.order_by("-top")
    paginator = Paginator(q, 15)
    page = request.GET.get("page")
    try:
        page = int(page)
        q = paginator.page(page)
    except:
        q = paginator.page(1)
        page = 1
    return render(request, "questions.html", {"q": q, "paginator": paginator, "page": page})


@login_need
def detail(request, id):
    user = get_current_user(request)
    if request.method == "POST":
        content = request.POST.get("content")
        if content and content != "":
            Answer.objects.create(users=user, content=content, question_id=int(id))
        return redirect("/detail/" + id + "/")
    question = Question.objects.get(id=int(id))
    flag = False
    collection = Collections.objects.filter(users=user).filter(question=question)
    if collection:
        flag = True
    LR = LikesRecord.objects.filter(users=user)
    q = Question.objects.all()
    # 热帖  喜欢最多
    hot_question1 = q.order_by("-comments")[:5]
    # 近期热议  收藏最多
    hot_question2 = q.order_by("-likes")[:5]
    return render(request, "detail.html", {"question": question, "id": id, "flag": flag, "LR": LR,
                                           "hot_question1": hot_question1, "hot_question2": hot_question2})


@login_need
#发布帖子
def add_question(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        bonus = request.POST.get("bonus")
        user = get_current_user(request)
        #当用户赏金不够的时候扣除其最所有赏金
        if user.bonus < int(bonus):
            bonus = user.bonus
            user.bonus = 0
        else:
            user.bonus -= int(bonus)
        user.save()
        question = Question.objects.create(users=user, title=title, content=content, bonus=bonus)
        return redirect("/detail/%s/" % question.id)
    return render(request, "add_question.html")


@login_need
# 置顶功能
def set_top(request):
    if request.method == "POST":
        id = request.POST["id"]
        flag = request.POST["flag"]
        question = Question.objects.get(id=int(id))
        question.top = flag
        question.save()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")

@login_need
# 删除帖子功能
def delete_question(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = get_current_user(request)
        if user.username == request.session["username"]:
            Question.objects.filter(id=int(id)).delete()
        else:
            errJson = initJson(success=False)
            errJson["detail"] = "无权限删除！"
            return HttpResponse(json.dumps(errJson), content_type="application/json")
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")


@login_need
# 收藏功能
def collection_question(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = get_current_user(request)
        flag = request.POST["flag"]
        if flag == "T":
            Collections.objects.create(users=user, question_id=int(id))
        else:
            Collections.objects.filter(users=user).filter(question_id=int(id)).delete()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")

@login_need
# 点赞功能
def like_answer(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = get_current_user(request)
        answer = Answer.objects.get(id=int(id))
        flag = LikesRecord.objects.filter(users=user).filter(answer=answer)
        if not flag:
            LikesRecord.objects.create(users=user, answer=answer)
            answer.likes += 1
        else:
            flag.delete()
            answer.likes -= 1
        answer.save()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")

@login_need
# 删除回答
def delete_answer(request):
    if request.method == "POST":
        id = request.POST["id"]
        answer = Answer.objects.get(id=int(id))
        answer.delete()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")


@login_need
# 采纳回答
def select_answer(request):
    if request.method == "POST":
        id = request.POST["id"]
        answer = Answer.objects.get(id=int(id))
        if answer.question.status == "T":
            errJson = initJson(success=False)
            errJson["detail"] = "不可重复采纳！"
            return HttpResponse(json.dumps(errJson), content_type="application/json")
        answer.status = "T"
        answer.question.status = "T"
        answer.question.save()
        answer.save()
        #赏金转移
        bonus = answer.question.bonus
        user = answer.users
        user.bonus += bonus
        user.save()
        return HttpResponse(json.dumps(initJson()), content_type="application/json")
    errJson = initJson(success=False)
    return HttpResponse(json.dumps(errJson), content_type="application/json")

@login_need
# 获取个人信息
def person_info(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = Users.objects.get(id=int(id))
        result = initJson()
        person = {
            "nickname":user.nickname,
            "bonus":user.bonus,
            "college":user.college,
            "major":user.major,
            "gender":user.get_gender(),
        }
        result["detail"] = person
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse("error!")