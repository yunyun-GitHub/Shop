from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.CartView.as_view({"post": "create", "get": "list"})),  # 獲取商品分類接口
    path('goods/<int:pk>/checked/', views.CartView.as_view({"put": "update_goods_status"})),  # 修改商品的選擇狀態
    path('goods/<int:pk>/number/', views.CartView.as_view({"put": "update_goods_number"})),  # 修改購物車商品數量
    path('goods/<int:pk>/', views.CartView.as_view({"delete": "destroy"})),  # 刪除購物車商品
]
