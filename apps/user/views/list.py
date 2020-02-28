import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.dataFilter import DataFilter
from django.core.paginator import Paginator, InvalidPage

from apps.user.models import User
from apps.user.serializers import UserSerializer


# 管理端视图
# url：user/list/
class UserList(APIView):
    """分页查询用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

        :param request:排序方式 当前页数 和每页显示的数目
        :return:
        """
        pageSize = request.GET.get('pageSize')
        sorter = request.GET.get('sorter')
        current = request.GET.get('current')
        id=request.GET.get('id')
        nickname=request.GET.get('nickname')
        user_status=request.GET.get('status')

        if id is None and nickname is None and user_status is None:
            # 如果排序方式为空或者无排序方式，就采用默认排序方式
            if sorter is None or sorter == '':
                queryset = User.objects.all().order_by("id")
            elif str(sorter).endswith('descend'):
                queryset = User.objects.all().order_by('-' + str(sorter).split("_")[0])
            else:
                queryset = User.objects.all().order_by(str(sorter).split("_")[0])
        #以下是分情况的查询
        elif id and nickname and user_status:
            queryset=User.objects.filter(id=id,nickname__contains=nickname,status=user_status)
        elif id and nickname:
            queryset = User.objects.filter(id=id, nickname__contains=nickname)
        elif id and user_status:
            queryset = User.objects.filter(id=id, status=user_status)
        elif nickname and user_status:
            queryset=User.objects.filter(nickname__contains=nickname,status=user_status)
        elif id:
            queryset = User.objects.filter(id=id)
        elif nickname:
            queryset = User.objects.filter(nickname__contains=nickname)
        else:
            queryset = User.objects.filter(status=user_status)
        if queryset is None:
            return Response({"data": "",
            "msg": True,
            "total":0,
            "pageSize": pageSize,
            "current": current},status=status.HTTP_200_OK)


        total = queryset.count()
        try:
            p = Paginator(queryset, pageSize)
            contacts = p.page(current).object_list
        except InvalidPage:
            return Response({"msg": "页码有错误"}, status=status.HTTP_400_BAD_REQUEST)
        # 从每一组数据中挑选出来

        serializer = UserSerializer(contacts, many=True)
        results = DataFilter.filter(serializer.data, 'id', 'openId', 'nickname', 'reimbursement', 'status',
                                    'latestSubmit')
        context = {
            "data": results,
            "msg": True,
            "total": total,
            "pageSize": pageSize,
            "current": current
        }
        return Response(context, status=status.HTTP_200_OK)
