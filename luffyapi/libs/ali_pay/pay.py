from alipay import AliPay
from alipay.utils import AliPayConfig
from . import settings

alipay = AliPay(
    appid=settings.APPID,
    app_notify_url=None,
    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
    sign_type=settings.SIGN_TYPE[0],
    debug=settings.DEBUG,
    verbose=False,
    config=AliPayConfig(timeout=15)
)
gateway = settings.GATEWAY

