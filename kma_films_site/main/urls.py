from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('votes/', views.VoteListView.as_view(), name='votes'),
    path('votes/<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('favorites/<int:pk>/', views.FavoriteDetailView.as_view(), name='favorite_detail'),
    path('csrf/', views.get_csrf_token, name='csrf'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='verify'),
    path('auth/register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
]
