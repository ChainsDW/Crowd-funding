from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
# Create your models here.


class Projects(models.Model):
    name = models.CharField(max_length=32, unique=True)
    sender = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=64)
    amount_goal = models.PositiveIntegerField(verbose_name='金额', default=10000)
    time_limit = models.DateField(auto_now_add=True)
    brief = models.TextField(verbose_name='项目简介')
    award = models.CharField(max_length=128, verbose_name='回报')
    goal = models.TextField(verbose_name='项目计划')
    file_adr = models.CharField(max_length=128, blank=True, null=True)
    status_choices = ((0, '未审核'),
                      (1, '审核中'),  #初步审核
                      (2, '审核通过'),
                      (3, '审核未通过'))
    status = models.SmallIntegerField(choices=status_choices, default=0)



class Batch(models.Model):
    Project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    batch = models.SmallIntegerField(verbose_name='批次')
    goal = models.TextField(verbose_name='阶段计划')


class UserInfo(models.Model):
    #用户信息表
    name = models.CharField(max_length=32)
    id_code = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=64, unique=True)


class Role(models.Model):
    #角色 发起人或投资人
    name = models.CharField(max_length=32, unique=True)


class UserAccount(models.Model):
    #账号表
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32, verbose_name='email', unique=True)
    password = models.CharField(max_length=64)
    role = models.ManyToManyField(Role)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class SendMsg(models.Model):
    #邮箱验证表
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=32, db_index=True)
    times = models.IntegerField(default=0)
    ctime = models.DateTimeField()
