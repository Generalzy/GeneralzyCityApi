from . import models
from rest_framework import serializers


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('name', 'role_name', 'title', 'signature', 'image', 'brief')


class CourseModelSerializer(serializers.ModelSerializer):
    # 子序列化
    teacher = TeacherModelSerializer()

    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'course_img',
            'brief',
            'attachment_path',
            'pub_sections',
            'price',
            'students',
            'period',
            'sections',
            'course_type_name',
            'level_name',
            'status_name',
            'teacher',
            'section_list',
        )
        # extra_kwargs={
        #
        # }
