import pytest
from rest_framework import status
from main.models import Movie

@pytest.mark.django_db
class TestMoviesAPI:
    def test_list_movies(self, api_client, sample_movie):
        response = api_client.get('/api/movies/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_movie(self, api_client, sample_movie):
        response = api_client.get(f'/api/movies/{sample_movie.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_movie_authenticated(self, authenticated_client):
        data = {
            'title': 'New Test Movie',
            'description': 'Description',
            'director': 'Director',
            'year': 2025,
            'rating': 9.0,
            'country': 'Ukraine',
            'genre': 'Drama'
        }
        response = authenticated_client.post('/api/movies/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_movie_unauthenticated(self, api_client):
        data = {
            'title': 'Unauthorized',
            'description': 'Test',
            'director': 'Test',
            'year': 2024,
            'rating': 7.0,
            'country': 'USA',
            'genre': 'Action'
        }
        response = api_client.post('/api/movies/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_movie_invalid(self, authenticated_client):
        data = {'title': '', 'year': 'not_a_number'}
        response = authenticated_client.post('/api/movies/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_movie_creator(self, authenticated_client, db):
        movie = Movie.objects.create(
            title='Original',
            description='Description',
            director='Director',
            year=2020,
            rating=7.0,
            country='USA',
            genre='Action',
            creator=authenticated_client.user
        )
        updated_data = {
            'title': 'Updated',
            'description': 'Updated Desc',
            'director': 'Director',
            'year': 2020,
            'rating': 8.5,
            'country': 'USA',
            'genre': 'Action'
        }
        response = authenticated_client.put(f'/api/movies/{movie.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_update_movie_non_creator(self, api_client, create_user, sample_movie):
        another_user = create_user(username='another', email='another@test.com')
        api_client.force_authenticate(user=another_user)
        updated_data = {
            'title': 'TryHack',
            'description': sample_movie.description,
            'director': sample_movie.director,
            'year': sample_movie.year,
            'rating': 10.0,
            'country': sample_movie.country,
            'genre': sample_movie.genre
        }
        response = api_client.put(f'/api/movies/{sample_movie.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_movie_creator(self, authenticated_client, db):
        movie = Movie.objects.create(
            title='To Be Deleted',
            description='Desc',
            director='Dir',
            year=2024,
            rating=7.0,
            country='USA',
            genre='Action',
            creator=authenticated_client.user
        )
        response = authenticated_client.delete(f'/api/movies/{movie.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Movie.objects.filter(id=movie.id).exists()

    def test_delete_movie_non_creator(self, api_client, create_user, sample_movie):
        hacker = create_user(username='hacker', email='hack@test.com')
        api_client.force_authenticate(user=hacker)
        response = api_client.delete(f'/api/movies/{sample_movie.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_nonexistent_movie(self, api_client):
        response = api_client.get('/api/movies/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_movie_creator(self, authenticated_client, sample_movie):
        url = f'/api/movies/{sample_movie.id}/'
        updated_data = {
            'title': 'Updated Title',
            'description': sample_movie.description,
            'director': sample_movie.director,
            'year': sample_movie.year,
            'rating': sample_movie.rating,
            'country': sample_movie.country,
            'genre': sample_movie.genre,
        }
        response = authenticated_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        sample_movie.refresh_from_db()
        assert sample_movie.title == 'Updated Title'

    def test_delete_movie_creator(self, authenticated_client, sample_movie):
        url = f'/api/movies/{sample_movie.id}/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Movie.objects.filter(id=sample_movie.id).exists()