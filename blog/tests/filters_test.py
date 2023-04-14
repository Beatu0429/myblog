import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post

@pytest.mark.django_db
class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post1 = Post.objects.create(
            title='Title 1',
            body='Body 1',
            author=self.user,
            safe=True,
        )
        self.post2 = Post.objects.create(
            title='Title 2',
            body='Body 2',
            author=self.user,
            safe=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_filter_by_safe(self):
        url = '/blog/api/post/?safe=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data[0]['title'], self.post1.title)

    def test_filter_by_user_id(self):
        url = f'/blog/api/post/?user={self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data[0]['title'], self.post1.title)
        self.assertEqual(response.data[1]['title'], self.post2.title)