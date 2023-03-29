import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from blog.models import Post, Comment

@pytest.mark.django_db
def test_comment_body_max_length(user):
    post = Post.objects.create(title='Test Post', body='Test body', author=user)
    comment = Comment.objects.create(blogpost=post)
    comment.body = 'a' * 256
    with pytest.raises(ValidationError, match='Ensure this value has at most 255 characters'):
        comment.full_clean()

@pytest.mark.django_db
def test_comment_mandatory_blogpost():
    with pytest.raises(IntegrityError):
        Comment.objects.create(body='Test comment body', user=None, blogpost=None)