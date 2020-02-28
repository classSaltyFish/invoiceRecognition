import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.models import User


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
        originHeads = request.META.get("HTTP_ORIGIN")  # 获取请求的主机地址
        headers = {
            'Access-Control-Allow-Origin': originHeads,
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Methods': 'POST, GET, PUT, OPTIONS, DELETE, PATCH',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'token,Origin, X-Requested-With, Content-Type, Accept,mid,X-Token'
        }
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
