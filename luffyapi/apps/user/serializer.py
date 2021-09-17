from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from user import models
import re


# 密码必须传入的序列化类
class UserModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32)

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if re.match(r'^1[3456789]\d{9}$', username):
            # 手机号
            user = models.User.objects.filter(telephone=username).first()
        elif re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', username):
            # 邮箱
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('该用户不存在')

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user
        return attrs


# 密码不需要传入的序列化类
class NoPasswordModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6, min_length=6)
    telephone=serializers.CharField(max_length=11)

    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    def _get_user(self, attrs):
        code = attrs.get('code')
        phone = attrs.get('telephone')
        cache_code = cache.get(settings.PHONE_CACHE_KEY % phone)
        if cache_code == code:
            if re.match(r'^1[3456789]\d{9}$', phone):
                user = models.User.objects.filter(telephone=phone).first()
                if user:
                    # 使用过的验证码删除
                    cache.set(settings.PHONE_CACHE_KEY % phone,'')
                    return user
                else:
                    raise ValidationError('用户不存在')
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['user'] = user
        return attrs
