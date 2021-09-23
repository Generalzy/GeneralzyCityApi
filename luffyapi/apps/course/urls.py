from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('categories', views.CourseCategoryView, basename='course')
router.register('free', views.CourseView, basename='free')
router.register('chapters', views.CourseChapterView, basename='chapters')
router.register('search',views.CourseSearchView,basename='search')

urlpatterns = [
    path('', include(router.urls))
]
