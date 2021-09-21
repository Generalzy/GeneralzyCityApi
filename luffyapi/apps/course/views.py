from django.shortcuts import render
from . import models
# Create your views here.
from luffyapi.utils.response import ApiResponse
from . import serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .paginations import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class CourseCategoryView(GenericViewSet, ListModelMixin):
    serializer_class = serializer.CourseCategoryModelSerializer
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).order_by('orders')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse(data=response.data)


class CourseView(GenericViewSet, ListModelMixin):
    serializer_class = serializer.CourseModelSerializer
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    pagination_class = PageNumberPagination

    # 过滤和排序
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # 排序
    ordering_fields = ['id', 'price', 'students']
    # 过滤
    filter_fields = ['course_category']
