from rest_framework import serializers
from ..models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['body', 'title', 'author', 'img', 'safe', 'comments_count', 'created_at', 'tagged_count', 'last_tag_date', 'tagged_users']


class BlogpostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['title', 'author']


class CommentSerializer(serializers.ModelSerializer):
    blogpost = BlogpostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'blogpost', 'user', 'created_at']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'blogpost', 'user']