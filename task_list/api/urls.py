from django.urls import path, include
from rest_framework import routers
from api import views


router_v1 = routers.DefaultRouter()

router_v1.register(r'auth/signup', views.SignUpViewSet, basename='signup')
router_v1.register(r'auth/token', views.TokenViewSet, basename='token')
router_v1.register(r'users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]