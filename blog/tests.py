from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from blog.models import Post

# Create your tests here.
@pytest.mark.django_db
class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpass')
        
    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            body='This is a test post content',
            author=self.user,
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.body, 'This is a test post content')
        self.assertEqual(post.author, self.user)

    def test_post_title_max_length(self):
        post = Post.objects.create(
            author= self.user,
            title='Lorem ipsum dolor sit amet.', 
            body='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
            )
        max_length = post._meta.get_field('title').max_length
        assert len(post.title) <= max_length

    def test_post_body_not_null(self):
        post = Post.objects.create(
            author= self.user,
            title='Lorem ipsum dolor sit amet.', 
            body='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
            )
        assert post.body != None
