import pytest
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Post
from blog.api.serializers import PostSerializer
from blog.views import PostsViewSet
from django.urls import reverse

@pytest.mark.django_db
def test_create_post(user):
    client = APIClient()
    url = reverse('blog:post-list')
    client.force_authenticate(user=user)
    data = {'title': 'Test Post', 'body': 'This is a test post'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Post.objects.get().title == 'Test Post'