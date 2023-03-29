import pytest
from django.contrib.auth.models import User
from django.test import Client
from blog.models import Post, Comment

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def post(user):
    return Post.objects.create(title='Test Post', body='This is a test post.', author=user)


@pytest.fixture
def comment(post, user):
    return Comment.objects.create(body='This is a test body.', blogpost=post, user=user)