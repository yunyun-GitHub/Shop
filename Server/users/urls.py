from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', views.LoginView.as_view()),          # 登錄
    path('register/', views.RegisterView.as_view()),    # 注冊
    path('token/refresh/', TokenRefreshView.as_view()),  # 刷新token
    path('token/verify/', TokenVerifyView.as_view()),    # 校驗token
    path('users/<int:pk>/', views.UserView.as_view({"get": "retrieve"})),    # 獲取單個用戶信息的路由
    path('<int:pk>/avatar/upload/', views.UserView.as_view({"post": "upload_avatar"})),    # 上傳用戶頭像的路由
    path('address/', views.AddrView.as_view({"get": "list", "post": "create"})),  # 添加地址和獲取地址列表的路由
    path('address/<int:pk>/', views.AddrView.as_view({"put": "update", "delete": "destroy"})),  # 修改收貨地址和刪除收貨地址
    path('address/<int:pk>/default/', views.AddrView.as_view({"put": "set_default_addr"})),  # 設置默認收貨地址
    path('sendsms/', views.SendSMSView.as_view()),  # 發送短信驗證碼的接口
    path('<int:pk>/mobile/bind/', views.UserView.as_view({"put": "bind_mobile"})),    # 綁定手機號
    path('<int:pk>/mobile/unbind/', views.UserView.as_view({"put": "unbind_mobile"})),    # 解綁手機號
    path('<int:pk>/name/', views.UserView.as_view({"put": "update_name"})),    # 修改用戶昵稱
    path('<int:pk>/email/', views.UserView.as_view({"put": "update_email"})),    # 修改用戶郵箱
    path('<int:pk>/password/', views.UserView.as_view({"put": "update_password"})),    # 修改用戶密碼
]
