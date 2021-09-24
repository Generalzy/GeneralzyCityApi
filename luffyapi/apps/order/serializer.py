from rest_framework import serializers
from order import models
from rest_framework.exceptions import ValidationError
import uuid
from django.conf import settings


class OrderModelSerializer(serializers.ModelSerializer):
    # 传过courses=[1,2,3] 处理成 coursers=[obj1,obj2,obj3]
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all(), write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['total_amount', 'subject', 'course', 'pay_type']
        extra_kwargs = {
            'pay_type': {
                'write_only': True,
                'required': True
            },
            'total_amount': {
                'write_only': True,
                'required': True
            }
        }

    def _check_total_amount(self, attrs):
        total_amount = attrs.get('total_amount')
        course_list = attrs.get('course')
        total_price = 0
        for course in course_list:
            total_price += course.price
        if total_amount != total_price:
            raise ValidationError('价格不合法')
        return total_price

    def create(self, validated_data):
        course_list = validated_data.pop('course')
        order = models.Order.objects.create(**validated_data)
        for course in course_list:
            models.OrderDetail.objects.create(order=order, course=course, price=course.price, real_price=course.price)
        return order

    def _get_out_trade_no(self):
        return str(uuid.uuid4())

    def _get_user(self):
        request = self.context.get('request')
        return request.user

    def _get_pay_url(self, out_trade_no, total_amount, subject):
        # total_amount是Decimal数据
        from luffyapi.libs.ali_pay import alipay, gateway
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=float(total_amount),
            subject=subject,
            return_url=settings.RETURN_URL,  # get 回调 前台地址
            notify_url=settings.NOTIFY_URL  # post回调 后台地址
        )
        return gateway + order_string

    def _before_create(self, attrs, user, pay_url, out_trade_no):
        attrs['user'] = user
        attrs['out_trade_no'] = out_trade_no
        self.context['pay_url'] = pay_url

    def validate(self, attrs):
        # 1）订单总价校验
        total_amount = self._check_total_amount(attrs)
        # 2）生成订单号
        out_trade_no = self._get_out_trade_no()
        # 3）支付用户：request.user
        user = self._get_user()
        # 4）支付链接生成
        if not total_amount == 0.00:
            pay_url = self._get_pay_url(out_trade_no, total_amount, attrs.get('subject'))
            # 5）入库(两个表)的信息准备
            self._before_create(attrs, user, pay_url, out_trade_no)
        # 代表该校验方法通过，进入入库操作
        else:
            import time
            attrs['user'] = user
            attrs['out_trade_no'] = out_trade_no
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            self.context[
                'pay_url'] = settings.RETURN_URL + '?charset=utf-8&out_trade_no=' + out_trade_no + '&total_amount=0' \
                                                                                                   '.00&trade_no=免费课&timestamp=' + timestamp
        return attrs
