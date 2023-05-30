from django.db import models
from common.db import BaseModel


class Cart(BaseModel):
    """購物車模型"""
    user = models.ForeignKey('users.User', help_text='用戶ID', verbose_name='用戶ID', on_delete=models.CASCADE, blank=True)
    goods = models.ForeignKey('goods.Goods', help_text='商品ID', verbose_name='商品ID', on_delete=models.CASCADE)
    number = models.SmallIntegerField(help_text='商品數量', verbose_name='商品數量', default=1, blank=True)
    is_checked = models.BooleanField(help_text='是否選中', verbose_name="是否選中",  default=True, blank=True)

    class Meta:
        db_table = 'cart'
        verbose_name = '購物車'
        verbose_name_plural = verbose_name
