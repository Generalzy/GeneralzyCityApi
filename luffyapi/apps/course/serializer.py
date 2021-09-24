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


class CourseSectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = ('name', 'section_link', 'duration', 'orders', 'free_trail', 'section_type_name')


class CourseChapterModelSerializer(serializers.ModelSerializer):
    # 一个章节下面可能有很多课时，要加many
    coursesections = CourseSectionModelSerializer(many=True)

    class Meta:
        model = models.CourseChapter
        fields = ('id', 'name', 'chapter', 'summary', 'coursesections')
