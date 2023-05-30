"""
訂單模塊序列化器
"""
from rest_framework import serializers

from goods.serializers import GoodsSerializer
from .models import Order, OrderGoods, Comment


class OrderSerializer(serializers.ModelSerializer):
    """訂單序列化器"""

    class Meta:
        model = Order
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    """訂單商品序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = ['goods', 'number', 'price']


class CommentSerializer(serializers.ModelSerializer):
    """評論序列化器"""

    class Meta:
        model = Comment
        fields = '__all__'
