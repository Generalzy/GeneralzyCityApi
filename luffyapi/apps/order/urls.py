from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
router.register('pay', views.PayView, 'pay')

urlpatterns = [
    path('', include(router.urls)),
    path('success/',views.SuccessView.as_view())
]
