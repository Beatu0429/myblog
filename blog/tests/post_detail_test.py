import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Post
import json

@pytest.mark.django_db
def test_retrieve_post(client, post):
    response = client.get(reverse('blog:post-detail', args=[post.pk]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == post.title
    assert response.data['body'] == post.body
    
@pytest.mark.django_db
def test_partial_update_post(client, post):
    new_data = {'title': 'New Title'}
    response = client.patch(
        reverse('blog:post-detail', args=[post.pk]),
        data=json.dumps(new_data),
        content_type='application/json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    post.refresh_from_db()
    assert post.title == 'New Title'
    
@pytest.mark.django_db
def test_delete_post(client, post):
    response = client.delete(reverse('blog:post-detail', args=[post.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Post.objects.filter(pk=post.pk).exists()