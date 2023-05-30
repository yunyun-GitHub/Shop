from django.contrib import admin
from .models import Order, OrderGoods, Comment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'order_code', 'pay_type', 'addr']


@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'price', 'number']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'goods', 'content', 'rate', 'star']
