# Generated by Django 2.0.3 on 2020-04-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_users_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='bonus',
            field=models.IntegerField(default=0, verbose_name='悬赏金额'),
        ),
    ]
