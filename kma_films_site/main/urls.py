from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('movies/', views.movies_list, name="movies_list"),
    path('movies/create/', views.movie_create, name="movie_create"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
