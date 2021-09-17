from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from user import models


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
        import re
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
