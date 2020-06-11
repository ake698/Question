from django.db import models


# Create your models here.

class Users(models.Model):
    status_choice = (
        ('T', '同意登陆'),
        ('F', '拒绝登陆'),
    )
    gender_choice = (
        ('T', '男'),
        ('F', '女'),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    nickname = models.CharField(max_length=10, verbose_name="昵称", default="新用户")
    username = models.CharField(max_length=10, unique=True, verbose_name="账号")
    img = models.ImageField(upload_to="img", verbose_name="用户头像", null=True, blank=True, default="default.jpg")
    password = models.CharField(max_length=10, verbose_name="密码")
    status = models.CharField(verbose_name="是否允许登陆", choices=status_choice, max_length=1, default="T")
    bonus = models.IntegerField(verbose_name="赏金", default=0)
    gender = models.CharField(max_length=1, choices=gender_choice, verbose_name="性别", default="T")
    college = models.CharField(max_length=10, verbose_name="院系", default="")
    major = models.CharField(max_length=20, verbose_name="专业", default="")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    def __str__(self):
        return self.username

    def get_gender(self):
        if self.gender == "T":
            return "男"
        return "女"

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = "用户管理"


class Question(models.Model):
    top_choice = (
        ("T", "置顶"),
        ("F", "不置顶"),
    )
    status_choice = (
        ("T", "已解决"),
        ("F", "未解决"),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="提问者")
    top = models.CharField(choices=top_choice, max_length=1, default="F", verbose_name="是否置顶")
    title = models.CharField(max_length=100, verbose_name="帖子标题")
    content = models.TextField(verbose_name="帖子内容")
    bonus = models.IntegerField(verbose_name="悬赏金额", default=10)
    likes = models.IntegerField(verbose_name="点赞数", default=0)
    comments = models.IntegerField(verbose_name="评论数", default=0)
    createTime = models.DateTimeField(auto_now=True, verbose_name="提问时间")
    status = models.CharField(choices=status_choice, max_length=1, default="F", verbose_name="是否解决")

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
    createTime = models.DateTimeField(auto_now=True, verbose_name="回复时间")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "回复管理"
        verbose_name_plural = "回复管理"

    def delete(self, using=None, keep_parents=False):
        super(Answer, self).delete()
        self.question.comments = self.question.answer_set.count()
        self.question.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Answer, self).save()
        self.question.comments = self.question.answer_set.count()
        self.question.save()


class Collections(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="回答者")
    createTime = models.DateTimeField(auto_now=True, verbose_name="收藏时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "收藏管理"
        verbose_name_plural = "收藏管理"


class LikesRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="问题")
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="用户")
    createTime = models.DateTimeField(auto_now=True, verbose_name="点在时间")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "点赞管理"
        verbose_name_plural = "点赞管理"
