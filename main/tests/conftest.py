import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from main.models import Movie

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(username=None, email=None, password="testpass123"):
        from uuid import uuid4
        uname = username or f"user_{uuid4().hex[:8]}"
        mail = email or f"{uname}@test.com"
        return User.objects.create_user(username=uname, email=mail, password=password)
    return make_user

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client

@pytest.fixture
def sample_movie(db, authenticated_client):
    return Movie.objects.create(
        title="Sample Movie",
        description="Desc",
        director="Dir",
        year=2024,
        rating=5.5,
        country="USA",
        genre="Action",
        creator=authenticated_client.user
    )
