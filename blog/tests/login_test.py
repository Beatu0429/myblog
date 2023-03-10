import pytest
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Post
from django.contrib.auth.models import User
from blog.api.serializers import PostSerializer
from blog import views


@pytest.fixture
def client():
    return Client()

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
def test_post_list():
    # Create a test user
    test_user = User.objects.create_user(
        username='testuser',
        password='testpass'
    )

    # Create some test posts with the test user as author
    Post.objects.create(author=test_user, title='Test Post 1', body='This is test post 1')
    Post.objects.create(author=test_user, title='Test Post 2', body='This is test post 2')

    # Make GET request to the PostList API view
    client = APIClient()
    url = reverse('blog:post-list')
    response = client.get(url)

    # Check if the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the response contains the correct number of posts
    expected_count = Post.objects.count()
    actual_count = len(response.data)
    assert actual_count == expected_count