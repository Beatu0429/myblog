import pytest
from django.urls import reverse
from django.test import Client


@pytest.fixture
def client():
    return Client()

def test_register(client):
    url = reverse('blog:register')
    response = client.get(url)
    assert response.status_code == 200


def test_login(client):
    url = reverse('blog:login')
    response = client.get(url)
    assert response.status_code == 200


def test_logout(client):
    url = reverse('blog:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('blog:index')