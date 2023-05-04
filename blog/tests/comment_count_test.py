import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from blog.models import Post, Comment


@pytest.fixture()
def post():
    return mixer.blend(Post)


@pytest.fixture()
def user():
    return mixer.blend(User)


@pytest.fixture()
def comment(post, user):
    return mixer.blend(Comment, blogpost=post, user=user)

@pytest.mark.django_db
def test_comments_count_property(post):
    assert post.comments_count == 0
    mixer.cycle(5).blend(Comment, blogpost=post)
    assert post.comments_count == 5
    mixer.cycle(3).blend(Comment)
    assert post.comments_count == 5
