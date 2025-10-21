from django.contrib import admin
from .models import Movie, Vote, Favorite

admin.site.register(Movie)
admin.site.register(Vote)
admin.site.register(Favorite)
