from django.shortcuts import render
from . import models
# Create your views here.
from luffyapi.utils.response import ApiResponse
from . import serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .paginations import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CourseCategoryView(GenericViewSet, ListModelMixin):
    serializer_class = serializer.CourseCategoryModelSerializer
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).order_by('orders')


class CourseView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = serializer.CourseModelSerializer
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    pagination_class = PageNumberPagination

    # 过滤和排序
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # 排序
    ordering_fields = ['id', 'price', 'students']
    # 过滤
    filter_fields = ['course_category']


class CourseChapterView(GenericViewSet, ListModelMixin):
    queryset = models.CourseChapter.objects.filter(is_delete=False, is_show=True)
    serializer_class = serializer.CourseChapterModelSerializer

    # 筛选指定课程的章节
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']


class CourseSearchView(GenericViewSet, ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination
    # 查询
    filter_backends = [SearchFilter]
    search_fields = ['name']
