"""
購物車模塊序列化器
"""
from rest_framework import serializers

from goods.serializers import GoodsSerializer
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    """寫入:購物車的序列化器"""

    class Meta:
        model = Cart
        fields = '__all__'


class ReadCartSerializer(serializers.ModelSerializer):
    """讀取:購物車信息的序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
