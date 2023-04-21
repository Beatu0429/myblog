import pytest
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from blog.models import Post, Like, Comment

@pytest.mark.django_db
def test_post_like_unique_constraint(post, user, like):
    content_type = ContentType.objects.get_for_model(Post)
    with pytest.raises(IntegrityError):
        Like.objects.create(user=user, content_type=content_type, object_id=post.id)


@pytest.mark.django_db
def test_comment_like_unique_constraint(comment, user, comment_like):
    content_type = ContentType.objects.get_for_model(Comment)
    with pytest.raises(IntegrityError):
        Like.objects.create(user=user, content_type=content_type, object_id=comment.id)