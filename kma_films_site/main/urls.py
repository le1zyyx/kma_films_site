from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('votes/', views.VoteListView.as_view(), name='votes'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
]
