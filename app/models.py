from django.db import models


# Create your models here.

class Users(models.Model):
    status_choice = (
        ('T', '同意登陆'),
        ('F', '拒绝登陆'),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    nickname = models.CharField(max_length=10, verbose_name="昵称", null=True, unique=True)
    username = models.CharField(max_length=10, unique=True, verbose_name="账号")
    img = models.ImageField(upload_to="file", verbose_name="用户头像", null=True, blank=True, default="file/default.jpg")
    password = models.CharField(max_length=10, verbose_name="密码")
    status = models.CharField(verbose_name="是否允许登陆", choices=status_choice, max_length=1, default="T")
    createTime = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = "用户管理"


class Question(models.Model):
    top_choice = (
        ("T", "置顶"),
        ("F", "不置顶"),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="提问者")
    top = models.CharField(choices=top_choice, max_length=1, default="F", verbose_name="是否置顶")
    title = models.CharField(max_length=100, verbose_name="帖子标题")
    content = models.TextField(verbose_name="帖子内容")
    bonus = models.IntegerField(verbose_name="悬赏金额")
    likes = models.IntegerField(verbose_name="点赞数", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "帖子管理"
        verbose_name_plural = "帖子管理"


class Answer(models.Model):
    status_choice = (
        ('T', '采纳'),
        ('F', '未采纳'),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="回答者")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    status = models.CharField(choices=status_choice, max_length=1, default="F", verbose_name="状态")
    content = models.TextField(verbose_name="回复内容")
    likes = models.IntegerField(verbose_name="点赞数", default=0)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "帖子管理"
        verbose_name_plural = "帖子管理"


class Collections(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="回答者")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "收藏管理"
        verbose_name_plural = "收藏管理"
