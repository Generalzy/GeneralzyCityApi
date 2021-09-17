from qcloudsms_py import SmsSingleSender
from luffyapi.utils.logger import log
from . import settings


def get_code():
    import random
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    return code


def send_messgae(phone, code):
    ssender = SmsSingleSender(settings.appid, settings.appkey)
    params = [code, '2']  # 当模板没有参数时，`params = []`,就是填短信时的{1} {2}
    try:
        result = ssender.send_with_param(86, phone,
                                         settings.template_id, params, sign=settings.sms_sign, extend="", ext="")
        if result.get('result'):
            return True
        else:
            return False
    except Exception as e:
        log.error('手机号:%s 短信发送失败,错误信息:%s' % (phone, str(e)))
