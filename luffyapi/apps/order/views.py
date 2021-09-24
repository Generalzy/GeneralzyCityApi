from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import models
from . import serializer


class PayView(GenericViewSet, CreateModelMixin):
    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    # 往两个表插入数据
    # 重写create方法
    # 生成订单 用uuid
    # 登录后才能做，加认证jwt
    # 取出当前登录用户
    # 传入request,必须重写create
    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        return Response(serializers.context.get('pay_url'))


class SuccessView(APIView):
    # 前端回调
    def get(self, request, *args, **kwargs):
        # < QueryDict: {'charset': ['utf-8'], 'out_trade_no': ['b851f091-5c36-4859-8be7-4bbb36ae543d'],
        #               'method': ['alipay.trade.page.pay.return'], 'total_amount': ['99.00'], 'sign': [
        #         'Jq0w8zpSuYadjznmykmzs9gJC/INirewLyPGsF3BA7V0b23nhwCGQEWiZNsfB+csGWlYhyIh2arR1w76XJjmmViXgXnp5l1jSslCQzNqKw8K0pXehP0hQSVtuXhkSPzDtVdiSi0QV+x4JrDIi4IQxA8Wg/6arRaNTuzSbV/KUOfGuUOOEC6cmSduQiRvcuVNSgHbuI82eZcW0jM5A8YrIQ5ePisVql6E1FoBtFDaLvg3048C2xOMIl3ujaL44fBHylZMeg4M7zvhgm2nplGVP+88sGmCnce3gNGdzf7rtKLaB/hVJz9AhffMu8br0dekc310ibQWj6fJzt/Oy5M3Tw=='],
        #               'trade_no': ['2021092422001480040501071995'], 'auth_app_id': ['2021000118621457'],
        #               'version': ['1.0'], 'app_id': ['2021000118621457'], 'sign_type': ['RSA2'],
        #               'seller_id': ['2088621956491045'], 'timestamp': ['2021-09-24 16:39:00']} >
        out_trade_no = request.GET.get('out_trade_no')
        order = models.Order.objects.filter(out_trade_no=out_trade_no).first()
        if order.order_status == 1:
            return Response(True)
        else:
            return Response(False)

    # 支付宝回调
    def post(self, request, *args, **kwargs):
        from luffyapi.utils.logger import log
        # request.data有两种可能
        # 1.字典
        # 2.query_set对象
        data = request.data.dict()
        out_trade_no = data.get('trade_no', None)
        pay_time = data.get('gmt_payment', None)
        sign = data.pop('sign')
        from luffyapi.libs.ali_pay import alipay
        success = alipay.verify(data, sign)
        if success and data['trade_status'] in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
            models.Order.objects.filter(put_trade_no=out_trade_no).update(order_status=1, pay_time=pay_time)
            log.info('%s 支付成功'%out_trade_no)
            return Response('success')
        else:
            return Response('error')
