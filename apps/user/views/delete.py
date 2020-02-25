from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from apps.invoice.models import Invoice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.serializers import UserSerializer
import json


# 管理端的删除用户视图
# url:user/deleteUser
class DeleteUser(APIView):
    """删除用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """

        :param request:要删除的用户的数组Key=[0,1,2,3]
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
            user.delete()
        return Response({'success': 'true'}, status=status.HTTP_200_OK)
