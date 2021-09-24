import os

APPID = "2021000118621457"

# 拼接路径
with open(os.path.join(os.path.dirname(__file__),'keys','app_private')) as f:
    APP_PRIVATE_KEY_STRING = f.read()
with open(os.path.join(os.path.dirname(__file__),'keys','alipay_public')) as f:
    ALIPAY_PUBLIC_KEY_STRING = f.read()

SIGN_TYPE = "RSA2",  # RSA or RSA2

DEBUG = True,  # False by default

GATEWAY = 'https://openapi.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi.alipay.com/gateway.do?'
