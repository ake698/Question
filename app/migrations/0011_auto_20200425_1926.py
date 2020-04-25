# Generated by Django 2.0.3 on 2020-04-25 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200425_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Question', verbose_name='问题'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='回答者'),
        ),
        migrations.AlterField(
            model_name='collections',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Question', verbose_name='问题'),
        ),
        migrations.AlterField(
            model_name='collections',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='回答者'),
        ),
        migrations.AlterField(
            model_name='likesrecord',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Answer', verbose_name='问题'),
        ),
        migrations.AlterField(
            model_name='likesrecord',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='question',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='提问者'),
        ),
    ]