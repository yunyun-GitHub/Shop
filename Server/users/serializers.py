from rest_framework import serializers
from users.models import User, Addr


class UserSerializer(serializers.ModelSerializer):
    """用戶模型的序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'avatar', 'last_name']


class AddSerializer(serializers.ModelSerializer):
    """收貨地址模型序列化器"""
    class Meta:
        model = Addr
        fields = '__all__'
