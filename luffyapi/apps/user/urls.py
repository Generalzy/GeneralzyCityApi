from django.urls import path, re_path,include
from rest_framework.routers import SimpleRouter
from . import views


router=SimpleRouter()
router.register('',views.LoginView,'login')


urlpatterns = [
    path('',include(router.urls))
]
