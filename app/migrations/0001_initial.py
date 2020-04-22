# Generated by Django 2.0.3 on 2020-04-22 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('T', '采纳'), ('F', '未采纳')], default='F', max_length=1, verbose_name='状态')),
                ('content', models.TextField(verbose_name='回复内容')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
            ],
            options={
                'verbose_name': '帖子管理',
                'verbose_name_plural': '帖子管理',
            },
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '收藏管理',
                'verbose_name_plural': '收藏管理',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('top', models.CharField(choices=[('T', '置顶'), ('F', '不置顶')], default='F', max_length=1, verbose_name='是否置顶')),
                ('title', models.CharField(max_length=100, verbose_name='帖子标题')),
                ('content', models.TextField(verbose_name='帖子内容')),
                ('bonus', models.IntegerField(verbose_name='悬赏金额')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
            ],
            options={
                'verbose_name': '帖子管理',
                'verbose_name_plural': '帖子管理',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=10, null=True, unique=True, verbose_name='昵称')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='账号')),
                ('img', models.ImageField(blank=True, default='file/default.jpg', null=True, upload_to='file', verbose_name='用户头像')),
                ('password', models.CharField(max_length=10, verbose_name='密码')),
                ('status', models.CharField(choices=[('T', '同意登陆'), ('F', '拒绝登陆')], default='T', max_length=1, verbose_name='是否允许登陆')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='提问者'),
        ),
        migrations.AddField(
            model_name='collections',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Question', verbose_name='问题'),
        ),
        migrations.AddField(
            model_name='collections',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='回答者'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Question', verbose_name='问题'),
        ),
        migrations.AddField(
            model_name='answer',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='回答者'),
        ),
    ]
