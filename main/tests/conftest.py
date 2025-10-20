import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from main.models import Movie

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(username="testuser", email="test@test.com", password="testpass123"):
        return User.objects.create_user(username=username, email=email, password=password)
    return make_user

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client

@pytest.fixture
def sample_movie(db, create_user):
    user = create_user(username="movieowner")
    return Movie.objects.create(
        title="Sample Movie",
        description="Sample Description",
        director="Sample Director",
        year=2024,
        rating=8.0,
        country="USA",
        genre="Action",
        creator=user
    )
