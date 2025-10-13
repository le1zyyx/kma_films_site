from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    director = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField()
    rating = models.FloatField()
    country = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=50, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_movies")
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(LIKE,'Like'),(DISLIKE,'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','movie')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','movie')
