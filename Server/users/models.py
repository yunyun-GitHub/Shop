from django.db import models
from common.db import BaseModel
from django.contrib.auth.models import AbstractUser  # django中自帶的用戶認證模型


class User(AbstractUser, BaseModel):
    """用戶模型"""
    mobile = models.CharField(verbose_name='手機號', default='', max_length=11)
    avatar = models.ImageField(verbose_name='用戶頭像', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用戶表'
        verbose_name_plural = verbose_name


class Addr(models.Model):
    """收貨地址模型"""
    user = models.ForeignKey('User', verbose_name='所屬用戶', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='手機號碼', max_length=11)
    name = models.CharField(verbose_name='聯係人', max_length=20)
    province = models.CharField(verbose_name='省份', max_length=20)
    city = models.CharField(verbose_name='城市', max_length=20)
    county = models.CharField(verbose_name='區縣', max_length=20)
    address = models.CharField(verbose_name='詳細地址', max_length=200)
    is_default = models.BooleanField(verbose_name='是否為默認地址', default=False)

    class Meta:
        db_table = 'addr'
        verbose_name = '收貨地址表'
        verbose_name_plural = verbose_name


class Area(models.Model):
    """省市區縣地址模型"""
    pid = models.IntegerField(verbose_name='上級id')
    name = models.CharField(verbose_name='地區名', max_length=20)
    level = models.CharField(verbose_name='區域等級', max_length=20)

    class Meta:
        db_table = 'area'
        verbose_name = '地區表'
        verbose_name_plural = verbose_name


class VerifCode(models.Model):
    """驗證碼模型"""
    mobile = models.CharField(verbose_name='手機號碼', max_length=11)
    code = models.CharField(max_length=6, verbose_name='驗證碼')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='生成時間')

    class Meta:
        db_table = 'verifcode'
        verbose_name = '手機驗證碼表'
        verbose_name_plural = verbose_name
