from django.contrib import admin
from django.contrib.auth.models import User,Group
from app.models import *
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ("id","username","password","nickname","status","createTime",)
    list_editable = ("status",)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id","users","top","title","bonus","likes","comments","status","createTime")

class AnsertAdmin(admin.ModelAdmin):
    list_display = ("id","question","users","status","likes","createTime")

admin.site.register(Users,UsersAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnsertAdmin)
admin.site.site_title = "问答分享平台管理后台"
admin.site.site_header = "问答分享平台管理后台"
admin.site.unregister(User)
admin.site.unregister(Group)