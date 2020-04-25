from django.http import HttpResponse
from django.shortcuts import render,redirect

from app.libs.initJson import initJson
from app.views import get_current_user
from app.models import Question,Collections
import json
# Create your views here.



def index(request):
    user = get_current_user(request)
    return render(request,"manager/user.html",{"user":user})


#修改个人信息
def modify(request):
    user = get_current_user(request)
    if request.method == "POST":
        nick_name = request.POST.get("nick_name")
        password = request.POST.get("password")
        img = request.FILES.get('vatar')
        #如果图片为空则代表不更新图片
        fileName = "default.jpg"
        if img !=None and img!="":
            from Question.settings import MEDIA_ROOT
            import os,time
            filesp = img.name.split(".")
            fileType = filesp[-1]
            if(fileType not in ["jpg","png","jpeg"]):
                errJson = initJson(success=False)
                errJson['detail'] = "错误的格式！"
                return HttpResponse(json.dumps(errJson),content_type="application/json")
            filesp.pop(-1)
            fileName = "%s_%s.%s"%("".join(filesp),int(round(time.time() * 1000)),fileType)
            f = open(os.path.join(MEDIA_ROOT,"img",fileName),'wb')
            for chunk in img.chunks():
                f.write(chunk)
            f.close()
        user.img = "img/%s"%fileName
        user.nickname = nick_name
        user.password = password
        user.save()
        #更新页面信息
        request.session["nickName"] = nick_name
        return HttpResponse(json.dumps(initJson()),content_type="application/json")
    return render(request,"manager/modiry.html",{"user":user})


#展示帖子
def question(request):
    user = get_current_user(request)
    q = Question.objects.filter(users=user)
    key = request.GET.get("Search")
    if key:
        q = q.filter(title__contains=key)
    return render(request,"manager/question.html",{"q":q})

#展示收藏的帖子
def likes(request):
    user = get_current_user(request)
    q = Collections.objects.filter(users=user)
    key = request.GET.get("Search")
    if key:
        q = q.filter(question__title__contains=key)
    return render(request,"manager/likes.html",{"q":q})