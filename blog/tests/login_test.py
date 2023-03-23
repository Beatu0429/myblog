import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Post
from blog.api.serializers import PostSerializer
from blog import views


def test_register(client):
    url = reverse('blog:register')
    response = client.get(url)
    assert response.status_code == 200


def test_login(client):
    url = reverse('blog:login')
    response = client.get(url)
    assert response.status_code == 200


def test_logout(client):
    url = reverse('blog:logout')
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_list(user):
    Post.objects.create(author=user, title='Test Post 1', body='This is test post 1')
    Post.objects.create(author=user, title='Test Post 2', body='This is test post 2')

    client = APIClient()
    url = reverse('blog:post-list')
    client.force_authenticate(user=user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_count = Post.objects.count()
    actual_count = len(response.data)
    assert actual_count == expected_count