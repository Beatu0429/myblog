from django.urls import path
from . import views
from rest_framework import routers

app_name = "blog" 

router = routers.DefaultRouter()
router.register(r'posts', views.PostsViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('api/post', views.PostsViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
]