from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Movie, Vote, Favorite
from .serializers import MovieSerializer, VoteSerializer, FavoriteSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly

def home(request):
    return HttpResponse("OK")

class MovieListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Movie, pk=pk)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        self.check_object_permissions(request, movie)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        self.check_object_permissions(request, movie)
        if Favorite.objects.filter(movie=movie).exists():
            return Response({'error': 'Cannot delete movie that is in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        if Vote.objects.filter(movie=movie).exists():
            return Response({'error': 'Cannot delete movie that has votes'}, status=status.HTTP_400_BAD_REQUEST)
        movie.delete()
        return Response({'message': 'Movie deleted'}, status=status.HTTP_204_NO_CONTENT)

class VoteListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteDetailView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Vote, pk=pk)

    def get(self, request, pk):
        vote = self.get_object(pk)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

    def put(self, request, pk):
        vote = self.get_object(pk)
        self.check_object_permissions(request, vote)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vote = self.get_object(pk)
        self.check_object_permissions(request, vote)
        vote.delete()
        return Response({'message': 'Vote deleted'}, status=status.HTTP_204_NO_CONTENT)

class FavoriteListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteDetailView(APIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Favorite, pk=pk)

    def get(self, request, pk):
        favorite = self.get_object(pk)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def put(self, request, pk):
        favorite = self.get_object(pk)
        self.check_object_permissions(request, favorite)
        serializer = FavoriteSerializer(favorite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        favorite = self.get_object(pk)
        self.check_object_permissions(request, favorite)
        favorite.delete()
        return Response({'message': 'Favorite deleted'}, status=status.HTTP_204_NO_CONTENT)
