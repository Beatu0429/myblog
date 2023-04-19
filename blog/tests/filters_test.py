import pytest
from django.urls import reverse
from rest_framework import status
from mixer.backend.django import mixer
from blog.models import Post

@pytest.mark.django_db
def test_filter_by_user(client, post, user):
    client.force_login(user=user)
    url = reverse('blog:post-list') + f'?user={user.id}'
    response = client.get(url)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1


@pytest.mark.django_db
def test_filter_by_safe(client, safe_post, unsafe_post, user):
    client.force_login(user=user)
    url = reverse('blog:post-list') + '?safe=True'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['author'] == user.username
    assert response.data['results'][0]['safe'] == safe_post.safe


@pytest.mark.django_db
def test_order_by_author(client, user):
    post1 = mixer.blend(Post, author=user)
    post2 = mixer.blend(Post, author=user)
    post3 = mixer.blend(Post, author=user)
    client.force_login(user=user)
    url = reverse('blog:post-list') + '?ordering=author'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_order_by_safe(client, user, safe_post, unsafe_post):
    client.force_login(user=user)
    url = reverse('blog:post-list') + '?ordering=safe'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['safe'] == unsafe_post.safe
    assert response.data['results'][1]['safe'] == safe_post.safe


@pytest.mark.django_db
def test_search(client, user):
    post1 = mixer.blend(Post, title='The quick brown fox', author=user)
    post2 = mixer.blend(Post, body='jumps over the lazy dog', author=user)
    post3 = mixer.blend(Post, author=user)
    client.force_login(user=user)
    url = reverse('blog:post-list') + '?search=quick'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == post1.title

    url = reverse('blog:post-list') + '?search=dog'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['body'] == post2.body

    url = reverse('blog:post-list') + '?search=brown+fox'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == post1.title


    url = reverse('blog:post-list') + '?search=xyz'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0