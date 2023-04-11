from django.urls import path, include
from . import views
from rest_framework import routers

app_name = "blog" 

router = routers.SimpleRouter()
router.register(r'post', views.PostsViewSet, basename='post')
router.register(r'comment', views.CommentsViewSet, basename='comment')

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('api/', include(router.urls)),
    path('api/post/my-tags/', views.PostsViewSet.as_view({'get': 'my_tags'}), name='my-tags'),
]