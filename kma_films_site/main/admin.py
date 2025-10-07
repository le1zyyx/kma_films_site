from django.contrib import admin
from .models import Movie, Vote, Favorite, Watchlist

admin.site.register(Movie)
admin.site.register(Vote)
admin.site.register(Favorite)
admin.site.register(Watchlist)
