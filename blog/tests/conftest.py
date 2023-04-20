import pytest
from django.contrib.auth.models import User
from django.test import Client
from blog.models import Post, Comment, UserTag, Like
from django.contrib.contenttypes.models import ContentType
from mixer.backend.django import mixer

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


@pytest.fixture
def users_list():
    return [
        mixer.blend('auth.User'),
        mixer.blend('auth.User'),
    ]

@pytest.fixture
def tagged_post(users_list):
    post = mixer.blend(Post)
    for user in users_list:
        mixer.blend(UserTag, post=post, user=user)
    return post

@pytest.fixture
def post_factory(author, title, body, safe=False):
    return Post.objects.create(
        author=author,
        title=title,
        body=body,
        safe=safe
    )


@pytest.fixture
def safe_post(user):
    return mixer.blend(Post, author=user, safe=True)


@pytest.fixture
def unsafe_post(user):
    return mixer.blend(Post, author=user, safe=False)

@pytest.fixture
def like(user, post):
    content_type = ContentType.objects.get_for_model(Post)
    return Like.objects.create(user=user, content_type=content_type, object_id=post.id)

@pytest.fixture
def comment_like(user, comment):
    content_type = ContentType.objects.get_for_model(Comment)
    return Like.objects.create(user=user, content_type=content_type, object_id=comment.id)