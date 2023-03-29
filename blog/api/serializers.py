from rest_framework import serializers
from ..models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['body', 'title', 'author', 'img', 'safe']


class BlogpostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['title', 'author']


class CommentSerializer(serializers.ModelSerializer):
    blogpost = BlogpostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'blogpost', 'user']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'blogpost', 'user']