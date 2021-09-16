from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
router.register('banner', views.BannerView)

urlpatterns = [
    # path('banner/',views.BannerView.as_view())
    path('', include(router.urls))
]
