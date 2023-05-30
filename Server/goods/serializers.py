"""
商品模塊序列化器
"""
from rest_framework import serializers
from .models import Goods, GoodsGroup, GoodsBanner, Detail, Collect


class GoodsSerializer(serializers.ModelSerializer):
    """商品模型的序列化器"""

    class Meta:
        model = Goods
        fields = '__all__'


class GoodsGroupSerializer(serializers.ModelSerializer):
    """商品分類模型序列化器"""

    class Meta:
        model = GoodsGroup
        fields = '__all__'


class GoodsBannerSerializer(serializers.ModelSerializer):
    """商品海報的序列化器"""

    class Meta:
        model = GoodsBanner
        fields = '__all__'


class DetailSerializer(serializers.ModelSerializer):
    """商品詳情的序列化器"""

    class Meta:
        model = Detail
        fields = '__all__'


class CollectSerializer(serializers.ModelSerializer):
    """商品收藏的序列化器"""

    class Meta:
        model = Collect
        fields = '__all__'
