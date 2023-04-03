import pytest
from mixer.backend.django import mixer
from django.utils import timezone
from blog.models import Post, UserTag

@pytest.mark.django_db
def test_post_tagged_count():
    post = mixer.blend(Post)
    user1 = mixer.blend('auth.User')
    user2 = mixer.blend('auth.User')
    mixer.blend(UserTag, post=post, user=user1)
    mixer.blend(UserTag, post=post, user=user2)
    assert post.tagged_count == 2

@pytest.mark.django_db
def test_post_last_tag_date():
    post = mixer.blend(Post)
    user1 = mixer.blend('auth.User')
    user2 = mixer.blend('auth.User')
    mixer.blend(UserTag, post=post, user=user1)
    mixer.blend(UserTag, post=post, user=user2)

    assert post.last_tag_date == timezone.now().date()
