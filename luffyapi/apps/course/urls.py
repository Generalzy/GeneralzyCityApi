from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('category', views.CourseCategoryView, basename='course')
router.register('free', views.CourseView, basename='free')

urlpatterns = [
    path('', include(router.urls))
]
