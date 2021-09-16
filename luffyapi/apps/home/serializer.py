from rest_framework import serializers
from home import models


class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ['name', 'link', 'img']
