"""
自定義用戶登錄的認證類,實現多字段登錄
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import User
from rest_framework import serializers


class MyBackend(ModelBackend):
    """自定義的登錄認證"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
        except:
            raise serializers.ValidationError({'error': "未找到該用戶"})
        else:
            # 驗證密碼是否正確
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({'error': "密碼不正塙"})
