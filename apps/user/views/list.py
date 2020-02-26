from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from apps.user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.dataFilter import DataFilter
from django.core.paginator import Paginator, InvalidPage
import json

# 管理端视图
# url：user/list/
class UserList(APIView):
    """分页查询用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''

        :param request:排序方式 当前页数 和每页显示的数目
        :return:
        '''
        originHeads = request.META.get("HTTP_ORIGIN")  # 获取请求的主机地址
        headers = {
            'Access-Control-Allow-Origin': originHeads,
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Methods': 'POST, GET, PUT, OPTIONS, DELETE, PATCH',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Headers': 'token,Origin, X-Requested-With, Content-Type, Accept,mid,X-Token'
        }

        data = json.load(request)
        pageSize = data['pageSize']
        sorter = data['sorter']
        current = data["page"]

        # 如果排序方式为空或者无排序方式，就采用默认排序方式
        if sorter is None or sorter == '':
            queryset = User.objects.all().order_by("id")
        elif str(sorter).endswith('descend'):
            queryset = User.objects.all().order_by('-' + str(sorter).split("_")[0])
        else:
            queryset = User.objects.all().order_by(str(sorter).split("_")[0])
        total = queryset.count()

        try:
            p = Paginator(queryset, pageSize)
            contacts = p.page(current).object_list
        except InvalidPage:
            return Response({"msg": "页码有错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,headers=headers)
        # 从每一组数据中挑选出来

        serializer=UserSerializer(contacts,many=True)
        results = DataFilter.filter(serializer.data, 'id', 'openId', 'nickname', 'reimbursement', 'status',
                                    'latestSubmit')
        context = {
            "data": results,
            "msg": True,
            "total": total,
            "pageSize": pageSize,
            "current": current
        }
        return Response(context, status=status.HTTP_200_OK,headers=headers)
