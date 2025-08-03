from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """用户表"""
    userId = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    isManager = models.BooleanField(default=False)  # 判断用户是否为管理者，可否登录后端系统
    avatar = models.ImageField(upload_to='avatar')