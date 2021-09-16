from django.utils.deprecation import MiddlewareMixin

from corsheaders.middleware import CorsMiddleware


class CORSMiddleWare(MiddlewareMixin):
    # 在响应中允许两个头
    def process_response(self, request, response):
        if request.method == "OPTIONS":
            # 可以加*
            response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Access-Control-Allow-Origin"] = "*"
        return response
