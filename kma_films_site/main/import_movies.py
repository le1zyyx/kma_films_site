import csv
from main.models import Movie
from django.contrib.auth.models import User

def import_movies():
    user = User.objects.first()
    with open('movies.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("Importing:", row)
            Movie.objects.create(
                title=row['title'],
                description=row['description'],
                director=row['director'],
                year=int(row['year']),
                rating=float(row['rating']),
                country=row['country'],
                genre=row['genre'],
                creator=user
            )
    print("Import completed")
