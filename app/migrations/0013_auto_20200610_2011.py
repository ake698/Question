# Generated by Django 2.0.3 on 2020-06-10 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20200610_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('T', '男'), ('F', '女')], default='T', max_length=1, verbose_name='性别'),
        ),
    ]
