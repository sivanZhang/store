# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 08:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(default='未填写', max_length=50, verbose_name='姓名')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='电子邮箱')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('is_admin', models.BooleanField(default=False, verbose_name='是否为管理员')),
                ('is_head_portrait', models.BooleanField(default=False, verbose_name='是否保存了上传后的头像')),
                ('head_portrait', models.ImageField(default='/media/portrait/no_img/no_portrait1.jpg', upload_to='portrait', verbose_name='选择头像')),
                ('email_verified', models.BooleanField(default=False, verbose_name='是否保存了邮箱')),
                ('social_user_status', models.IntegerField(default=0, verbose_name='第三方用户状态')),
                ('social_site_name', models.IntegerField(default=0, verbose_name='第三方名称')),
                ('social_user_id', models.CharField(default='未填写', max_length=255, verbose_name='第三方用户ID')),
                ('thumbnail_portait', models.ImageField(default='/media/portrait/no_img/no_portrait1.jpg', upload_to='portrait', verbose_name='头像缩略图')),
                ('msg_mark', models.BooleanField(default=False, verbose_name='有新消息')),
            ],
            options={
                'permissions': (('admin_management', 'manage group, permission and user'),),
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('code', models.CharField(default='', max_length=50, verbose_name='code')),
                ('type', models.CharField(default='0', max_length=5, verbose_name='type')),
            ],
        ),
        migrations.CreateModel(
            name='AdaptorUser',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appuser.BaseUser')),
            ],
            options={
                'db_table': 'user',
            },
            bases=('appuser.baseuser',),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
