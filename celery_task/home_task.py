from .celery import app
from django.core.cache import cache


@app.task
def banner_update():
    from home import serializer
    from home import models
    from django.conf import settings

    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('display_order')[
               :settings.BANNER_COUNT]
    banner_ser = serializer.BannerModelSerializer(instance=queryset, many=True)
    for banner in banner_ser:
        banner['img'] = 'http://127.0.0.1:8000' + banner['img']
    cache.set('banner_list', banner_ser.data)
    return True
