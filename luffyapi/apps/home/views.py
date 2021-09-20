from home import models
from home import serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response


# class BannerView(GenericAPIView, ListModelMixin):
# 继承方式灵活
# 当前路由配置 : path('', include(router.urls))
class BannerView(GenericViewSet, ListModelMixin):
    # 限定只展示三条
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('display_order')[
               :settings.BANNER_COUNT]
    serializer_class = serializer.BannerModelSerializer

    def list(self, request, *args, **kwargs):
        banner_list = cache.get('banner_list')
        if not banner_list:
            # 缓存中没有
            response = super().list(request, *args, **kwargs)
            cache.set('banner_list', response.data)
            return Response(data=response.data)
        return Response(data=banner_list)
