import time

from django.db import transaction
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cart.models import Cart
from common.pay import Pay
from users.models import Addr
from .models import Order, OrderGoods, Comment
from .permissions import OrderPermission
from .serializers import OrderSerializer, OrderGoodsSerializer, CommentSerializer


class OrderView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]  # 設置認證用戶才能有權限訪問
    filterset_fields = ('status',)

    @transaction.atomic  # 對整個視圖的操作開啓事務(數據庫)
    def create(self, request, *args, **kwargs):
        """提交訂單視圖"""
        addrId = request.data.get('addrId')  # 前端只需要傳一個地址ID
        if not (addr := Addr.objects.filter(user=request.user, id=addrId).first()):  # 用戶的收穫地址是否在地址列表中
            return Response({'error': "訂單提交失敗,收貨地址有誤"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 收穫地址用字符串保存,如果用模型對象保存一旦收貨地址變化,訂單中的地址也會變化.
        addr_str = '{}{}{}{} {} {}'.format(addr.province, addr.city, addr.county, addr.address, addr.name, addr.phone)
        cart_goods = Cart.objects.filter(user=request.user, is_checked=True)  # 查詢購物車商品
        if not cart_goods.exists():
            return Response({'error': "訂單提交失敗,未選中商品"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order_code = str(int(time.time())) + str(request.user.id)  # 生產訂單編號

        # 設置一個事務保存的節點
        save_id = transaction.savepoint()
        try:
            # 創建一個訂單(有些字段先不填)
            order = Order.objects.create(user=request.user, addr=addr_str, order_code=order_code, amount=0)
            amount = 0
            for cart in cart_goods:  # 遍歷購物車中的商品
                amount += cart.goods.price * cart.number
                if cart.goods.stock > cart.number:   # 購買的數量是否超過該商品庫存
                    cart.goods.stock -= cart.number  # 修改數據庫該商品庫存和銷量
                    cart.goods.sales += cart.number
                    cart.goods.save()  # 保存該商品數據
                else:
                    # 事務回滾
                    transaction.savepoint_rollback(save_id)
                    return Response({'error': "訂單提交失敗,商品{}庫存不足".format(cart.goods.title)},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                # 創建一條訂單商品表數據(因爲一個訂單對應多個商品)
                OrderGoods.objects.create(order=order, goods=cart.goods, price=cart.goods.price, number=cart.number)
                # 刪除購物車中該商品
                cart.delete()
            order.amount = amount  # 修改訂單縂金額
            order.save()
        except Exception as e:  # Exception表示有任何類型的錯誤
            # 事務回滾
            transaction.savepoint_rollback(save_id)
            return Response({'error': e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:  # 提交事務保存數據到數據庫
            transaction.savepoint_commit(save_id)
            # 返回結果
            ser = self.get_serializer(order)
            return Response({'message': ser.data}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """獲取訂單列表"""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """獲取訂單詳情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 獲取訂單中的商品信息
        order_goods = OrderGoods.objects.filter(order=instance)
        order_goods_serializer = OrderGoodsSerializer(order_goods, many=True)

        result = serializer.data
        result['goods_list'] = order_goods_serializer.data
        return Response(result)

    def close_order(self, request, *args, **kwargs):
        """取消訂單"""
        obj = self.get_object()
        if obj.status != 1:
            return Response({'error': "只能取消未支付的訂單"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        obj.status = 6
        obj.save()
        return Response({'message': '取消訂單成功'}, status=status.HTTP_200_OK)


class CommentView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    """商品评价的接口"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ('goods', 'order')

    def create(self, request, *args, **kwargs):
        """商品评价的接口"""
        if not (order := request.data.get('order')):
            return Response({'error': "訂單ID不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not (order_obj := Order.objects.filter(id=order, user=request.user).first()):
            return Response({'error': "訂單不存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if order_obj.status != 4:
            return Response({'error': "訂單不處於待評論狀態"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 获取订单评论详情参数
        comment = request.data.get('comment')
        if not isinstance(comment, list):
            return Response({'error': "訂單comment格式有误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        for item in comment:
            # 遍历参数中的商品评论信息
            # 校验参数是否有误
            if not isinstance(item, dict):
                return Response({'error': "訂單comment格式有误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # 添加评论
            goods = item.get('goods', None)
            if not OrderGoods.objects.filter(order=order_obj, goods=goods).exists():
                return Response({'error': "订单中没有id为{}的商品".format(goods)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            item['user'] = request.user.id
            item['goods'] = goods
            ser = CommentSerializer(data=item)
            ser.is_valid(raise_exception=True)
            ser.save()
        order.status = 5
        order.save()
        return Response({'message': '评论成功'}, status=status.HTTP_200_OK)


class OrderPayView(GenericViewSet):
    """订单支付接口"""
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """支付"""
        orderId = request.data.get('orderId')  # 前端只需要傳一個订单ID
        if not (orderObj := self.get_queryset().filter(id=orderId, user=request.user).first()):
            return Response({'error': "訂單不存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        order_on = orderObj.order_code  # 获取订单编号
        amount = str(orderObj.amount)  # 获取订单金额
        pay_url = Pay.alipay(order_on, amount)  # 生成支付宝支付的页面地址

        return Response({'pay_url': pay_url}, status=status.HTTP_201_CREATED)
