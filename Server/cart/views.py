from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cart.models import Cart
from cart.permissions import CartPermission
from cart.serializers import CartSerializer, ReadCartSerializer


class CartView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
               mixins.DestroyModelMixin):
    """購物車視圖集"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, CartPermission]  # 設置認證用戶才能有權限訪問

    def get_serializer_class(self):
        """實現讀寫操作使用不同的序列化器"""
        if self.action == 'list':
            return ReadCartSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """添加商品到購物車"""
        # 獲取參數
        user = request.user  # 直接獲取登錄的用戶,不需要前端傳user字段
        goods = request.data.get('goods')
        # 1,校驗該用戶的購物車中是否有該商品
        if cart_goods := self.get_queryset().filter(user=user, goods=goods).first():
            # 這個用戶已經添加過該商品到購物車,直接修改商品數量
            cart_goods.number += 1
            cart_goods.save()
            # 對該商品進行序列化
            serializer = self.get_serializer(cart_goods)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 從後端獲取登錄的用戶,不需要前端傳user字段
        request.data['user'] = user.id
        return super().create(request, *args, **kwargs)  # 調用父類方法進行創建

    def list(self, request, *args, **kwargs):
        """獲取用戶購物車的所有商品"""
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update_goods_status(self, request, *args, **kwargs):
        """修改商品的選擇狀態"""
        obj = self.get_object()
        obj.is_checked = not obj.is_checked
        obj.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def update_goods_number(self, request, *args, **kwargs):
        """修改商品的數量"""
        number = request.data.get('number')
        obj = self.get_object()
        if not number or not isinstance(number, int):
            return Response({'error': "參數number只能為int類型,并且不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if number <= 0:
            # 刪除該商品
            obj.delete()
            return Response({'message': '修改成功,該商品數量為0,已從購物車移除'}, status=status.HTTP_200_OK)
        elif number > obj.goods.stock:
            return Response({'error': "數量不能超過庫存"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            obj.number = number
            obj.save()
            return Response({'message': '修改成功'}, status=status.HTTP_200_OK)
