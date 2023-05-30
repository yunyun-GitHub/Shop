import random
import re
import time

from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.aliyun_sms import AliyunSMS
from users.models import User, Addr, VerifCode
from users.permissions import UserPermission, AddrPermission
from users.serializers import UserSerializer, AddSerializer


class RegisterView(APIView):
    def post(self, request):
        """注冊接口"""
        # 1,接收用戶參數
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        password_confirmation = request.data.get('password_confirmation')
        # 2,校驗參數
        # 校驗參數是否爲空
        if not all([username, password, email, password_confirmation]):
            return Response({'error': "所有參數不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 檢驗用戶名是否已注冊
        if User.objects.filter(username=username).exists():
            return Response({'error': "用戶名已存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 檢驗兩次密碼是否一致
        if password != password_confirmation:
            return Response({'error': "兩次密碼不一致"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校驗密碼長度
        if not (6 <= len(password) <= 18):
            return Response({'error': "密碼長度要在6到18位之間"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校驗郵箱
        if User.objects.filter(email=email).exists():
            return Response({'error': "該郵箱已被其他用戶使用"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not re.match(r'^[a-z\d][\w.\-]*@[a-z\d\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': "郵箱格式有誤"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 3,創建用戶
        obj = User.objects.create_user(username=username, email=email, password=password)
        res = {"username": username, "id": obj.id, 'email': obj.email}
        return Response(res, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """用戶登錄"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定義登錄成功之後返回的結果
        result = serializer.validated_data
        result['token'] = result.pop('access')
        result['id'] = serializer.user.id
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username

        return Response(result, status=status.HTTP_200_OK)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    """用戶相關操作的視圖集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]  # 設置認證用戶才能有權限訪問

    def upload_avatar(self, request, *args, **kwargs):
        """上傳用戶頭像"""
        avatar = request.data.get("avatar")
        # 校驗是否有上傳文件
        if not avatar:
            return Response({'error': "上傳失敗,文件不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校驗文件大小不能超過300k
        if avatar.size > 1024 * 300:
            return Response({'error': "上傳失敗,文件大小不能超過300kb"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 保存文件
        user = self.get_object()
        user.avatar.field.upload_to = f"{user.username}/avatar"  # 修改upload_to属性动态保存图片路径
        ser = self.get_serializer(user, data={"avatar": avatar}, partial=True)  # partial表示可以只傳一部分數據
        # 校驗
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'url': ser.data['avatar']})

    def bind_mobile(self, request, *args, **kwargs):
        """綁定手機號"""
        # 校驗驗證碼
        if result := self.verif_code(request):  # 驗證碼校驗通用邏輯
            return result

        # 4,綁定手機號
        mobile = request.data.get("mobile")  # 綁定手機號
        # 校驗手機號
        if User.objects.filter(mobile=mobile).exists():
            return Response({'error': "該手機號已被用戶綁定"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 綁定手機號
        # user = self.get_object()
        user = request.user
        user.mobile = mobile
        user.save()
        return Response({'message': "綁定手機號!"}, status=status.HTTP_200_OK)

    def unbind_mobile(self, request, *args, **kwargs):
        """解綁手機號"""
        # 校驗驗證碼
        if result := self.verif_code(request):  # 驗證碼校驗通用邏輯
            return result

        # 解綁手機(驗證用戶已綁定手機號)
        mobile = request.data.get("mobile")  # 綁定手機號
        user = request.user
        if user.mobile != mobile:
            return Response({'error': "該手機號沒有被當前用戶綁定"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user.mobile = ''
        user.save()
        return Response({'message': "解綁手機號成功!"}, status=status.HTTP_200_OK)

    def update_name(self, request, *args, **kwargs):
        """修改用戶昵稱"""
        # 1,獲取參數
        last_name = request.data.get("last_name")
        # 校驗參數
        if not last_name:
            return Response({'error': "參數last_name不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 修改用戶名
        user = self.get_object()
        user.last_name = last_name
        user.save()
        return Response({'message': "修改用戶昵稱成功!"}, status=status.HTTP_200_OK)

    def update_email(self, request, *args, **kwargs):
        """修改用戶郵箱"""
        # 1,獲取參數
        email = request.data.get('email')
        # 2,校驗參數
        if not email:
            return Response({'error': "郵箱不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not re.match(r'^[a-z\d][\w.\-]*@[a-z\d\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': "郵箱格式有誤"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if User.objects.filter(email=email).exists():
            return Response({'error': "該郵箱已被用戶使用"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 修改用戶郵箱
        user = self.get_object()
        user.email = email
        user.save()
        return Response({'message': "修改用戶郵箱成功!"}, status=status.HTTP_200_OK)

    def update_password(self, request, *args, **kwargs):
        """修改用戶密碼"""
        # 1,獲取參數
        user = self.get_object()
        mobile = request.data.get("mobile")  # 綁定手機號
        password = request.data.get("password")  # 綁定手機號
        password_confirmation = request.data.get("password_confirmation")  # 綁定手機號

        # 校驗驗證碼
        if result := self.verif_code(request):  # 驗證碼校驗通用邏輯
            return result
        if user.mobile != mobile:
            return Response({'error': "此驗證碼驗不是該用戶綁定手機發送的驗證碼"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not password:
            return Response({'error': "密碼不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            return Response({'error': "兩次密碼不一致"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 修改密碼
        user.set_password(password)  # 密碼在數據庫中是加密存儲的,修改密碼必須要使用用戶的set_password方法
        user.save()
        return Response({'message': "修改用戶密碼成功!"}, status=status.HTTP_200_OK)

    @staticmethod
    def verif_code(request):
        """驗證碼校驗通用邏輯"""
        # 1,獲取參數
        code = request.data.get("code")  # 獲取驗證碼
        codeID = request.data.get("codeID")  # 獲取驗證碼ID
        mobile = request.data.get("mobile")  # 綁定手機號

        # 2,校驗參數
        if not code:
            return Response({'error': "驗證碼不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not codeID:
            return Response({'error': "驗證碼ID不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not mobile:
            return Response({'error': "手機號不能爲空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 3,校驗驗證碼
        if c_obj := VerifCode.objects.filter(id=codeID, code=code, mobile=mobile).first():  # 驗證碼存在
            # 校驗驗證碼是否過期(過期時間3分鐘)
            ct = c_obj.create_time.timestamp()  # 獲取驗證碼創建時間, timestamp()表示轉換為時間戳
            et = time.time()  # 獲取當前時間戳
            # 刪除驗證碼(避免用戶在有效期内,使用同一個驗證碼重複請求)
            c_obj.delete()
            if et - ct >= 60 * 3:
                return Response({'error': "驗證碼已過期,請重新獲取驗證碼"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({'error': "驗證碼驗證失敗,請重新獲取驗證碼"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AddrView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
               mixins.UpdateModelMixin):
    """收貨地址管理視圖"""
    queryset = Addr.objects.all()
    serializer_class = AddSerializer
    permission_classes = [IsAuthenticated, AddrPermission]  # 設置認證用戶才能有權限訪問

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 通過請求過來的認證用戶進行過濾
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_addr(self, request, *args, **kwargs):
        """設置默認收貨地址"""
        # 1,獲取到要設置的地址對象
        obj = self.get_object()
        obj.is_default = True
        obj.save()
        # 2,將該地址設置默認收貨地址,將用戶的其他收貨地址設置為非默認
        # 獲取用戶收貨地址
        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        return Response({'message': "設置成功!"}, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    """發送短信驗證碼"""
    throttle_classes = (AnonRateThrottle,)  # 設置限流(每分鐘只能獲取一次)

    def post(self, request):
        # 獲取手機號碼
        mobile = request.data.get('mobile', '')  # 第二個參數''表示如果沒有則為空,即爲默認值
        # 驗證手機號碼格式是否正確(正則表達式匹配)
        res = re.match(r'^(13\d|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18\d|19[0-35-9])\d{8}$', mobile)
        if not res:
            return Response({'error': "無效的手機號碼"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 隨機生成一個6位數驗證碼
        code = self.get_random_code()
        # 發送短信驗證碼
        result = AliyunSMS().send(mobile=mobile, code=code)
        if result['code'] == 'OK':
            # 將短信驗證碼入庫
            obj = VerifCode.objects.create(mobile=mobile, code=code)
            result['codeID'] = obj.id
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_random_code():
        """隨機生成一個6位數驗證碼"""
        # code2 = ''.join([str(random.choice(range(10))) for i in range(6)])
        code = ''
        for i in range(6):
            n = random.choice(range(10))
            code += str(n)
        return code
