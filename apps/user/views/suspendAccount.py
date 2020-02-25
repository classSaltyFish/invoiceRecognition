from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


# 管理端视图
# url:user/suspend/
class SuspendUser(APIView):
    """冻结用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        :param request:要冻结的用户的数组Key=[0,1,2,3]
        :return:
        """
        data = json.load(request)
        key = data['key']
        for i in key:
            userid = i
            try:
                user = User.objects.get(id=userid)
            # 如果用户不存在的话，返回错误信息
            except User.DoesNotExist:
                return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
            user.status = 0
            user.save()
        return Response({'msg': 'true'}, status=status.HTTP_200_OK)


# 管理端视图
# url:user/unsuspend
class UnSuspendUser(APIView):
    """解冻用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        :param request:要解冻的用户的数组Key=[0,1,2,3]
        :return:
        """
        data = json.load(request)
        key = data['key']
        for i in key:
            userid = i
            try:
                user = User.objects.get(id=userid)
                # 如果用户不存在的话，返回错误信息
            except User.DoesNotExist:
                return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
            user.status=1
            user.save()
        return Response({'msg': 'true'}, status=status.HTTP_200_OK)
