from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:  # 判斷登錄的賬號是否是管理員
            return True
        return obj == request.user  # 如果不是管理員,則判斷操作的用戶對象和登錄的用戶對象是否是同一個用戶


class AddrPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        name = view.__class__.__module__ + '.' + view.__class__.__name__ + '.' + view.action
        print(name)
        return True

    def has_object_permission(self, request, view, obj):
        # view表示当前视图, obj為具體的當前要操作的一條數據對象
        if request.user.is_superuser:  # 判斷登錄的賬號是否是管理員
            return True
        return obj.user == request.user  # 如果不是管理員,則判斷操作的用戶對象和登錄的用戶對象是否是同一個用戶
