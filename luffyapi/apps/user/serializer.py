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
    telephone = serializers.CharField(max_length=11)

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
                    cache.set(settings.PHONE_CACHE_KEY % phone, '')
                    return user
                else:
                    raise ValidationError('用户不存在')
            else:
                raise ValidationError('手机号格式错误')
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


# 注册
class RegisterModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6, min_length=6, write_only=True)
    telephone = serializers.CharField(max_length=11, min_length=11,write_only=True)

    class Meta:
        model = models.User
        fields = ['telephone', 'password', 'code', 'username']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 18,
                'min_length': 8,
            },
            'username': {
                'read_only': True
            }
        }

    def validate_telephone(self, telephone):
        if re.match(r'^1[3456789]\d{9}$', telephone):
            return telephone
        else:
            raise ValidationError('手机号格式错误')

    # 上线用
    # def validate(self, attrs):
    #     code = attrs.get('code')
    #     phone = attrs.get('telephone')
    #     user = models.User.objects.filter(telephone=phone).first()
    #     if user:
    #         raise ValidationError('该用户已存在，请勿重复注册')
    #     else:
    #         cache_code = cache.get(settings.PHONE_CACHE_KEY % phone)
    #         if cache_code == code:
    #             attrs['username'] = phone  # 将username设置成phone
    #             attrs.pop('code')          # 将code pop 出去
    #             return attrs
    #         else:
    #             raise ValidationError('验证码错误')
    # 测试用
    def validate(self, attrs):
        code = attrs.get('code')
        phone = attrs.get('telephone')
        user = models.User.objects.filter(telephone=phone).first()
        if user:
            raise ValidationError('该用户已存在，请勿重复注册')
        else:
            cache_code = '520520'
            if cache_code == code:
                attrs['username'] = phone  # 将username设置成phone
                attrs.pop('code')  # 将code pop 出去
                return attrs
            else:
                raise ValidationError('验证码错误')

    # 原生的create 方法会将所有参数传入，会报错
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
