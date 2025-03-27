from rest_framework import viewsets

from apps.movies.models import Country, Genre, Director, Movie
from .serializers import CountrySerializer, GenreSerializer, DirectorSerializer, MovieSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    """
    queryset = Country.objects.all().order_by("country")
    serializer_class = CountrySerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows genres to be viewed or edited.
    """
    queryset = Genre.objects.all().order_by("genre")
    serializer_class = GenreSerializer


class DirectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows directors to be viewed or edited.
    """
    queryset = Director.objects.all().order_by("director")
    serializer_class = DirectorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all().order_by("-kp_rating")
    serializer_class = MovieSerializer
    # permission_classes = [permissions.IsAuthenticated]
