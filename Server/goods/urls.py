from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view()),  # 商城首頁數據獲取
    path('goods/', views.GoodsView.as_view({"get": "list"})),  # 商品列表接口
    path('goods/<int:pk>/', views.GoodsView.as_view({"get": "retrieve"})),  # 獲取單個商品接口
    path('collect/', views.CollectView.as_view({"post": "create", "get": "list"})),  # 收藏商品,獲取收藏列表
    path('collect/<int:pk>/', views.CollectView.as_view({"delete": "destroy"})),  # 取消收藏商品接口
    path('group/', views.GoodsGroupView.as_view({"get": "list"})),  # 獲取商品分類接口
]
