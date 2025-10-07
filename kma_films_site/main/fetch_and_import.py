import requests
from main.models import Movie
from django.contrib.auth.models import User

API_KEY = '965bacf3'
SEARCH_TERMS = ['star', 'war', 'love', 'man', 'girl']
RESULTS_PER_TERM = 50

def fetch_and_import():
    user = User.objects.first()
    imported = 0

    for term in SEARCH_TERMS:
        page = 1
        while page * 10 <= RESULTS_PER_TERM:
            resp = requests.get(
                'http://www.omdbapi.com/',
                params={'apikey': API_KEY, 's': term, 'page': page}
            ).json()
            for item in resp.get('Search', []):
                detail = requests.get(
                    'http://www.omdbapi.com/',
                    params={'apikey': API_KEY, 'i': item['imdbID'], 'plot': 'short'}
                ).json()
                Movie.objects.update_or_create(
                    title=detail.get('Title',''),
                    defaults={
                        'description': detail.get('Plot',''),
                        'director': detail.get('Director',''),
                        'year': int(detail.get('Year','0')[:4] or 0),
                        'rating': float(detail.get('imdbRating') or 0),
                        'country': detail.get('Country',''),
                        'genre': detail.get('Genre',''),
                        'creator': user
                    }
                )
                imported += 1
            page += 1

    print(f"Imported {imported} movies")
