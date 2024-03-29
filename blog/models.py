from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    body = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='uploads/images/%Y/%m/%d/', blank=True, null=True)
    safe = models.BooleanField(default=True)
    tagged_users = models.ManyToManyField(User, through='UserTag', related_name='tagged_posts')
    likes = GenericRelation('Like', related_query_name='likes')

    @property
    def comments_count(self):
        return self.comment_set.count()
    
    @property
    def tagged_count(self):
        return self.tagged_users.count()

    @property
    def last_tag_date(self):
        last_tag = self.usertag_set.order_by('-created_at').first()
        return last_tag.created_at.date() if last_tag else None
    
    def __str__(self):
        return self.title
    

class UserTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    body = models.CharField(max_length=255)
    blogpost = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = GenericRelation('Like', related_query_name='likes')
    def __str__(self):
        return self.body


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} liked {self.content_type.model} {self.object_id}"