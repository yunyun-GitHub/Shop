from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.OrderView.as_view({"post": "create"})),  # 提交訂單
    path('order/', views.OrderView.as_view({"get": "list"})),  # 獲取訂單列表
    path('order/<int:pk>/', views.OrderView.as_view({"get": "retrieve", "put": "close_order"})),  # 獲取訂單詳情
    path('comment/', views.CommentView.as_view({"post": "create", "get": "list"})),  # 商品评价
    path('alipay/', views.OrderPayView.as_view({"post": "create"})),  # 订单支付页面地址获取
]
