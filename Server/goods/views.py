from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from goods.models import GoodsGroup, GoodsBanner, Goods, Collect, Detail
from goods.permissions import CollectPermission
from goods.serializers import GoodsSerializer, GoodsGroupSerializer, GoodsBannerSerializer, CollectSerializer, \
    DetailSerializer


class IndexView(APIView):
    """商城首頁數據獲取接口"""

    def get(self, request):
        # 獲取商品所有分類信息
        group = GoodsGroup.objects.filter(status=True)
        # 序列化如果有圖片字段,返回數據需要補全完整的域名,需要傳入請求對象context={'request': request}
        group_ser = GoodsGroupSerializer(group, many=True, context={'request': request})
        # 獲取商品的海報圖
        banner = GoodsBanner.objects.filter(status=True)
        banner_ser = GoodsBannerSerializer(banner, many=True, context={'request': request})
        # 獲取所有的推薦商品
        goods = Goods.objects.filter(recommend=True)
        goods_ser = GoodsSerializer(goods, many=True, context={'request': request})

        result = dict(
            group=group_ser.data,
            banner=banner_ser.data,
            goods=goods_ser.data,
        )
        return Response(result, status=status.HTTP_200_OK)


class GoodsView(ReadOnlyModelViewSet):
    """商品視圖集"""
    queryset = Goods.objects.filter(is_on=True)
    serializer_class = GoodsSerializer
    filterset_fields = ('group', 'recommend')  # 實現通過商品分類和是否推薦進行過濾
    ordering_fields = ('sales', 'price')  # 實現通過價格和銷量排序

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 獲取商品詳情
        detail = Detail.objects.filter(goods=instance).first()
        detail_ser = DetailSerializer(detail)
        # 返回結果
        result = serializer.data
        result['detail'] = detail_ser.data
        return Response(result)


class CollectView(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """收藏商品和取消收藏,收藏列表"""
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated, CollectPermission]  # 設置認證用戶才能有權限訪問

    def create(self, request, *args, **kwargs):
        """收藏商品"""
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)  # 調用父類方法進行創建

    def list(self, request, *args, **kwargs):
        """獲取收藏列表"""
        queryset = self.filter_queryset(self.get_queryset())
        # 通過請求過來的認證用戶進行過濾
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GoodsGroupView(mixins.ListModelMixin, GenericViewSet):
    """商品分類視圖集"""
    queryset = GoodsGroup.objects.filter(status=True)
    serializer_class = GoodsGroupSerializer
