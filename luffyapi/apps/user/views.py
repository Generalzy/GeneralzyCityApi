from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from luffyapi.utils.response import ApiResponse
from rest_framework.decorators import action
from django.conf import settings
from . import models
import re


# Create your views here.
class LoginView(ViewSet):
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        from . import serializer
        user_ser = serializer.UserModelSerializer(data=request.data)
        if user_ser.is_valid():
            token = user_ser.context['token']
            username = user_ser.context['user'].username
            return ApiResponse(token=token, username=username)
        else:
            return ApiResponse(code=0, msg=user_ser.errors)

    # @action(methods=['GET'], detail=False)
    # def check_phone(self, request, *args, **kwargs):
    #     phone = request.GET.get('phone')
    #     if not re.match(r'^1[3456789]\d{9}$', phone):
    #         return ApiResponse(code=0, msg='手机号不合法')
    #
    #     if models.User.objects.filter(telephone=phone).first():
    #         return ApiResponse(result=True)
    #     else:
    #         return ApiResponse(result=False)

    @action(methods=['POST'], detail=False)
    def check_phone(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if not re.match(r'^1[3456789]\d{9}$', phone):
            return ApiResponse(code=0, msg='手机号不合法')
        if models.User.objects.filter(telephone=phone).first():
            return ApiResponse()
        else:
            return ApiResponse(code=0, msg='手机号不存在')

    @action(methods=['POST'], detail=False)
    def send(self, request, *args, **kwargs):
        from luffyapi.libs.tencent.sends import send_messgae, get_code
        from django.core.cache import cache
        phone = request.data.get('phone')
        if not re.match(r'^1[3456789]\d{9}$', phone):
            return ApiResponse(code=0, msg='手机号不合法')
        code = get_code()
        result = send_messgae(phone, code) # 返回true 或者 false
        # cache.set(settings.PHONE_CACHE_KEY % phone, code)
        if result:
            cache.set(settings.PHONE_CACHE_KEY % phone, code, 120)
            return ApiResponse(msg='验证码发送成功')
        else:
            return ApiResponse(code=0, msg='验证码发送失败')
