from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from apps.user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from utils.dataFilter import DataFilter


# 用户分页器
class UserPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 6


# 管理端视图
# url：user/list/
class UserList(APIView):
    """分页查询用户"""
    # 测试用
    # permission_classes = (AllowAny,)

    # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

        :param request:排序方式 当前页数 和每页显示的数目
        :return:
        """
        pageSize = request.GET.get('pagesize')
        sorter = request.GET.get('sorter')
        # 如果排序方式为空或者无排序方式，就采用默认排序方式
        if sorter is None or sorter == '':
            queryset = User.objects.all().order_by("id")
        else:
            queryset = User.objects.all().order_by(sorter)

        total = queryset.count()
        current = request.GET.get("page")

        page = UserPagination()
        UserPagination.page_size = pageSize
        page_roles = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = UserSerializer(page_roles, many=True)
        # 从每一组数据中挑选出来
        data = DataFilter.filter(serializer.data, 'id', 'openId', 'nickname', 'reimbursement', 'status', 'latestSubmit')
        context = {
            "results": data,
            "msg": True,
            "total": total,
            "pageSize": pageSize,
            "current": current
        }
        return Response(context, status=status.HTTP_200_OK)
