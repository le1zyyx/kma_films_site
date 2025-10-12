from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('votes/', views.VoteListView.as_view(), name='votes'),
    path('votes/<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('favorites/<int:pk>/', views.FavoriteDetailView.as_view(), name='favorite_detail'),
]
