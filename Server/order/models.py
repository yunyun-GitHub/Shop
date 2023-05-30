from django.db import models
from common.db import BaseModel


class Order(BaseModel):
    """訂單表"""
    ORDER_STATUS = ((1, '待支付'), (2, '代發貨'), (3, '配送中'), (4, '待評價'), (5, '已完成'), (6, '已關閉'))
    PAY_TYPES = ((1, '支付寶'), (2, '微信支付'), (3, '雲閃付'), (4, '貨到付款'))
    user = models.ForeignKey('users.User', verbose_name='下單用戶', help_text='下單用戶', on_delete=models.CASCADE)
    addr = models.CharField(verbose_name='收貨地址', help_text='收貨地址', max_length=200)
    order_code = models.CharField(verbose_name='訂單編號', help_text='訂單編號', max_length=50)
    amount = models.FloatField(verbose_name='訂單總金額', help_text='訂單總金額')
    status = models.SmallIntegerField(verbose_name='訂單狀態', help_text='訂單狀態', default=1, choices=ORDER_STATUS)
    pay_type = models.SmallIntegerField(verbose_name='支付方式', help_text='支付方式', blank=True, null=True, choices=PAY_TYPES)
    pay_time = models.DateTimeField(verbose_name='支付時間', help_text='支付時間', blank=True, null=True)
    trade_no = models.CharField(verbose_name='支付單號', help_text='支付單號', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'order'
        verbose_name = '訂單表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_code


class OrderGoods(BaseModel):
    """訂單商品表"""
    order = models.ForeignKey('Order', verbose_name='所屬訂單', help_text='所屬訂單', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name='商品ID', help_text='商品ID', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='商品價格', help_text='商品價格')
    number = models.IntegerField(verbose_name='商品數量', help_text='商品數量', default=1)
    # iscomment = models.BooleanField(verbose_name="是否評價", default=False)

    class Meta:
        db_table = 'orderGoods'
        verbose_name = '訂單詳情'
        verbose_name_plural = verbose_name


class Comment(BaseModel):
    """訂單評論表"""
    RATES = ((1, '好評'), (2, '中評'), (3, '差評'))
    STARS = ((1, '一星'), (2, '二星'), (3, '三星'), (4, '四星'), (5, '五星'))
    user = models.ForeignKey('users.User', verbose_name='評論用戶', help_text='評論用戶', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name='所屬訂單', help_text='所屬訂單', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name='所屬商品', help_text='所屬商品', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='評論内容', help_text='評論内容', default='', max_length=500)
    rate = models.SmallIntegerField(verbose_name='評論級別', help_text='評論級別', default=1, choices=RATES, blank=True)
    star = models.SmallIntegerField(verbose_name='評論星級', help_text='評論星級', default=5, choices=STARS, blank=True)

    class Meta:
        db_table = 'comment'
        verbose_name = '訂單評論'
        verbose_name_plural = verbose_name
