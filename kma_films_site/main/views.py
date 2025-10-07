from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie, Vote, Favorite, Watchlist
from .serializers import MovieSerializer, VoteSerializer, FavoriteSerializer, WatchlistSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("OK")

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        if Favorite.objects.filter(movie=movie).exists():
            return Response({'error': 'Cannot delete movie that is in favorites'}, status=400)
        if Vote.objects.filter(movie=movie).exists():
            return Response({'error': 'Cannot delete movie that has votes'}, status=400)
        movie.delete()
        return Response({'message': 'Movie deleted'}, status=204)

class VoteListView(APIView):
    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FavoriteListView(APIView):
    def get(self, request):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VoteDetailView(APIView):
    def get(self, request, pk):
        try:
            vote = Vote.objects.get(id=pk)
        except Vote.DoesNotExist:
            return Response({'error': 'Vote not found'}, status=404)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            vote = Vote.objects.get(id=pk)
        except Vote.DoesNotExist:
            return Response({'error': 'Vote not found'}, status=404)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            vote = Vote.objects.get(id=pk)
        except Vote.DoesNotExist:
            return Response({'error': 'Vote not found'}, status=404)
        vote.delete()
        return Response({'message': 'Vote deleted'}, status=204)

class FavoriteDetailView(APIView):
    def get(self, request, pk):
        try:
            favorite = Favorite.objects.get(id=pk)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=404)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            favorite = Favorite.objects.get(id=pk)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=404)
        serializer = FavoriteSerializer(favorite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.get(id=pk)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=404)
        favorite.delete()
        return Response({'message': 'Favorite deleted'}, status=204)
