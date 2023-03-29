from django.urls import path
from . import views

app_name = "blog" 

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('api/post/', views.PostsViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('api/post/<int:pk>/', views.PostsViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-detail'),
    path('api/comment/', views.CommentsViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('api/comment/<int:pk>/', views.CommentsViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment-detail'),
]