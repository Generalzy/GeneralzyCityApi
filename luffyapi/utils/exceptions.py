from rest_framework import status
from rest_framework.views import exception_handler
from luffyapi.utils import response
from .logger import log

from corsheaders.middleware import CorsMiddleware


# 写日志
# from . import response 从当前路径导入response
def common_exception_handler(exc, context):
    # context['view'] 是TextView的对象
    # context['view'].__class__.__name__拿出错误的类
    log.error('view视图: %s-------error错误: %s' % (context['view'].__class__.__name__, str(exc)))
    res = exception_handler(exc, context)  # res是个Response对象,内部有个data
    if not res:
        # 系统处理不了的，直接返回
        return response.ApiResponse(code=0, msg='error', result=str(exc),status=status.HTTP_400_BAD_REQUEST)
    else:
        # 已知错误，顺手给data返回
        return response.ApiResponse(code=0, msg='error', result=res.data,status=status.HTTP_400_BAD_REQUEST)
