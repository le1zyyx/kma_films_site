from django.http import JsonResponse
from .models import Movie
from .serializers import MovieSerializer

def movies_list(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return JsonResponse(data, safe=False)

def movie_create(request):
    if request.method == "POST":
        import json
        from django.views.decorators.csrf import csrf_exempt
        @csrf_exempt
        def inner(request):
            data = json.loads(request.body)
            m = Movie.objects.create(
                title=data.get("title", ""),
                description=data.get("description", ""),
                director=data.get("director", ""),
                year=data.get("year", 2023),
                rating=data.get("rating", 0.0),
                country=data.get("country", ""),
                genre=data.get("genre", ""),
                creator=request.user
            )
            return JsonResponse(MovieSerializer(m).data)
        return inner(request)
    return JsonResponse({"error": "Тільки POST"}, status=400)
