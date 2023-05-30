from ckeditor.fields import RichTextField
from django.db import models
from common.db import BaseModel


class GoodsGroup(models.Model):
    """商品分類表"""
    name = models.CharField(max_length=20, verbose_name="名稱")
    image = models.ImageField(blank=True, null=True, verbose_name="分類圖標")
    status = models.BooleanField(default=False, verbose_name="是否啓用")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_group'
        verbose_name = '商品分類表'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """商品"""
    group = models.ForeignKey('GoodsGroup', verbose_name='分類', help_text='分類', max_length=20, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='標題', help_text='標題', max_length=200, default='')
    desc = models.CharField(verbose_name='商品描述', help_text='商品描述', max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品價格', help_text='商品價格')
    cover = models.ImageField(verbose_name='封面圖鏈接', help_text='封面圖鏈接', blank=True, null=True)
    stock = models.IntegerField(default=1, verbose_name='庫存', help_text='庫存', blank=True)
    sales = models.IntegerField(default=0, verbose_name='銷量', help_text='銷量', blank=True)
    is_on = models.BooleanField(default=False, verbose_name="是否上架", help_text='是否上架', blank=True)
    recommend = models.BooleanField(default=False, verbose_name="是否推薦", help_text='是否推薦', blank=True)

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Detail(BaseModel):
    """商品詳情"""
    goods = models.OneToOneField('Goods', verbose_name='商品', on_delete=models.CASCADE)
    producer = models.CharField(verbose_name='廠商', help_text='廠商', max_length=200)
    norms = models.CharField(verbose_name='規格', help_text='規格', max_length=200)
    # pip install django-ckeditor
    details = RichTextField(blank=True, verbose_name='商品詳情')

    class Meta:
        db_table = 'detail'
        verbose_name = '商品詳情'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.goods


class GoodsBanner(BaseModel):
    """商品輪播圖"""
    title = models.CharField(verbose_name='輪播圖名稱', help_text='輪播圖名稱', max_length=20, default='')
    image = models.ImageField(verbose_name='輪播圖鏈接', help_text='輪播圖鏈接', blank=True, null=True)
    status = models.BooleanField(verbose_name="是否啓用", help_text='是否啓用', default=False, blank=True)
    seq = models.IntegerField(verbose_name='順序', help_text='順序', default=1, blank=True)

    class Meta:
        db_table = 'banner'
        verbose_name = '首頁商品輪播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Collect(models.Model):
    """收藏商品"""
    user = models.ForeignKey('users.User', verbose_name='用戶ID', help_text='用戶ID', on_delete=models.CASCADE, blank=True)
    goods = models.ForeignKey('Goods', verbose_name='商品ID', help_text='商品ID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'collect'
        verbose_name = '收藏商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods
